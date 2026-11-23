"""WeightBench pilot verifier, wbp-f-ss3: Q3 on held-out PDB chains.

reward = clip((metric - BASELINE) / (TOP - BASELINE), 0, 1), rounded to 9 decimals. A missing or invalid
submission, or one whose canonical (float64) outputs are not finite, is the writer's failure: reward 0 with the
reason in reward-details.json. Missing or altered private data, or any other evaluator error, raises before a
reward is written: the trial is unscored (infrastructure) and relaunched.

The canonical forward pass is float64 NumPy. A float32 pass runs too; how often its prediction differs is
recorded (float32_disagreement) and never changes the reward. Argmax: logits within 1e-9 * max(1, |max|) of the
row maximum count as tied, and ties go to the lowest index.
"""
import hashlib
import json
import math
import os
import platform
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, '/verifier')
from check_submission import check  # noqa: E402

SUBMISSION = Path('/app/submission/model.safetensors')
SPEC = Path('/verifier/spec.json')
PRIVATE = Path('/verifier/private')
LOGS = Path('/logs/verifier')
PRIVATE_SHA256 = {
    "heldout.json": "bb08c2aba79d51e96415c79fc8c19bcf1d6fe21bf8ea3123a4eb4e6091738fa0"
}
BASELINE = 0.408926396
TOP = 0.68816294
TIE = 1e-9


class NonFinite(Exception):
    pass


def sha(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def private(name):
    path = PRIVATE / name
    if not path.is_file():
        raise RuntimeError(f'missing private file {name}: the verifier cannot grade (unscored)')
    if sha(path) != PRIVATE_SHA256[name]:
        raise RuntimeError(f'private file {name} differs from its pinned sha256 (unscored)')
    return path


def argmax_low(logits):
    best = logits.max(axis=-1, keepdims=True)
    return np.argmax(logits >= best - TIE * np.maximum(1.0, np.abs(best)), axis=-1)


def cpu_model():
    try:
        with open('/proc/cpuinfo') as info:
            for line in info:
                if line.startswith('model name'):
                    return line.split(':', 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or 'unknown'


def finish(reward, details):
    LOGS.mkdir(parents=True, exist_ok=True)
    (LOGS / 'reward-details.json').write_text(json.dumps(details, indent=1, sort_keys=True) + '\n')
    (LOGS / 'reward.json').write_text(json.dumps({'reward': reward}) + '\n')
    print(json.dumps({'reward': reward, 'status': details['status'], 'metric': details.get('metric')}))


def main():
    started = time.time()
    environment = dict(cpu_model=cpu_model(), python=platform.python_version(), numpy=np.__version__,
                       pins={k: os.environ.get(k) for k in ('OPENBLAS_CORETYPE', 'NPY_DISABLE_CPU_FEATURES',
                                                            'OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS')})
    for name in PRIVATE_SHA256:  # infrastructure first: missing or altered private data raises (unscored)
        private(name)
    validity = check(SUBMISSION, SPEC)
    if not validity['valid']:
        finish(0.0, dict(status='submission_failed', reason='invalid_or_missing_submission', check=validity,
                         environment=environment))
        return
    from safetensors.numpy import load_file
    digest = sha(SUBMISSION)
    weights = load_file(str(SUBMISSION))
    try:
        with np.errstate(over='ignore', invalid='ignore', divide='ignore'):
            result = evaluate(weights)
    except NonFinite as error:
        finish(0.0, dict(status='submission_failed', reason='nonfinite_outputs', where=str(error),
                         submission_sha256=digest, check=validity, environment=environment))
        return
    metric = round(result.pop('metric'), 9)
    score = min(1.0, max(0.0, (metric - BASELINE) / (TOP - BASELINE)))
    finish(round(score, 9), dict(status='scored', metric_name=METRIC, metric=metric, baseline=BASELINE, top=TOP,
                                 normalised=score, submission_sha256=digest, check=validity, details=result,
                                 environment=environment, verifier_seconds=time.time() - started))

METRIC = 'q3'

AA = 'ACDEFGHIKLMNPQRSTVWY'
SCORED = 223248
CHUNK = 20000

def mlp(w, x, dtype, layers):
    x = x.astype(dtype)
    for i in range(1, layers + 1):
        x = x @ w[f'fc{i}.weight'].astype(dtype).T + w[f'fc{i}.bias'].astype(dtype)
        if i < layers:
            x = np.maximum(x, 0)
    return x


def windows(chains):
    lookup = {c: i for i, c in enumerate(AA)}
    codes, labels = [], []
    for seq, states in chains:
        c = np.array([lookup.get(ch, 20) for ch in seq], np.int64)
        padded = np.concatenate([np.full(7, 21), c, np.full(7, 21)])
        codes.append(np.stack([padded[j:j + len(seq)] for j in range(15)], axis=1))
        labels.append(np.array(['HEC-'.index(ch) for ch in states], np.int64))  # 3: no coordinates, not scored
    return np.concatenate(codes), np.concatenate(labels)


def onehot(codes):
    x = np.zeros((len(codes), 15, 22))
    x[np.arange(len(codes))[:, None], np.arange(15)[None, :], codes] = 1
    return x[:, :, :21].reshape(len(codes), 315)


def evaluate(w):
    chains = json.loads(private('heldout.json').read_text())
    if len(chains) != 1000 or any(len(s) != len(t) for s, t in chains):
        raise RuntimeError('held-out set is not 1,000 chains with one state per residue')
    codes, y = windows(chains)
    scored = y < 3
    counts = np.bincount(y[scored], minlength=3)
    if (len(y) != 248783 or int(scored.sum()) != SCORED or int(counts.argmax()) != 2
            or round(float(counts[2] / scored.sum()), 9) != BASELINE):
        raise RuntimeError('held-out residues, scored residues or coil share differ from the stated ones')
    codes, y = codes[scored], y[scored]
    correct = differ = 0
    per_class = np.zeros(3, np.int64)
    for start in range(0, len(y), CHUNK):
        x, t = onehot(codes[start:start + CHUNK]), y[start:start + CHUNK]
        l64 = mlp(w, x, np.float64, 3)
        if not np.isfinite(l64).all():
            raise NonFinite('float64 logits')
        pred = argmax_low(l64)
        correct += int((pred == t).sum())
        np.add.at(per_class, t[pred == t], 1)
        differ += int((argmax_low(mlp(w, x, np.float32, 3)) != pred).sum())
    totals = np.bincount(y, minlength=3)
    return dict(metric=correct / len(y), correct=correct, residues=len(y), chains=len(chains),
                recall_per_state=dict(zip('HEC', [round(float(a / b), 6) for a, b in zip(per_class, totals)])),
                float32_disagreement=differ / len(y))


if __name__ == '__main__':
    main()

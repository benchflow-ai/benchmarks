"""WeightBench pilot verifier, wbp-f-splice: accuracy on held-out splice-site windows.

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
    "heldout.json": "23b7cac9b841bfda7f37192e06ff5755be9ae024c6362ff098fbd4a850ae668d"
}
BASELINE = 0.5
TOP = 0.85375
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

METRIC = 'accuracy'

BATCH = 2000

def mlp(w, x, dtype, layers):
    x = x.astype(dtype)
    for i in range(1, layers + 1):
        x = x @ w[f'fc{i}.weight'].astype(dtype).T + w[f'fc{i}.bias'].astype(dtype)
        if i < layers:
            x = np.maximum(x, 0)
    return x


def classify(forward, w, x, y, batch, classes):
    correct = differ = 0
    per_class = np.zeros(classes, np.int64)
    for start in range(0, len(y), batch):
        xb, yb = x[start:start + batch], y[start:start + batch]
        l64 = forward(w, xb, np.float64)
        if not np.isfinite(l64).all():
            raise NonFinite('float64 logits')
        pred = argmax_low(l64)
        correct += int((pred == yb).sum())
        np.add.at(per_class, yb[pred == yb], 1)
        differ += int((argmax_low(forward(w, xb, np.float32)) != pred).sum())
    totals = np.bincount(y, minlength=classes)
    recall = (per_class / np.maximum(totals, 1)).tolist()
    return dict(accuracy=correct / len(y), correct=correct, items=len(y), correct_per_class=per_class.tolist(),
                items_per_class=totals.tolist(), recall_per_class=[round(r, 6) for r in recall],
                balanced_accuracy=float(np.mean(recall)), float32_disagreement=differ / len(y))


def forward(w, x, dtype):
    return mlp(w, x, dtype, 3)


def evaluate(w):
    rows = json.loads(private('heldout.json').read_text())
    lut = np.full(256, -1, np.int64)
    for i, c in enumerate(b'ACGT'):
        lut[c] = i
    codes = np.stack([lut[np.frombuffer(s.encode(), np.uint8)] for s, _, _ in rows])
    y = np.array([label for _, label, _ in rows], np.int64)
    kinds = [kind for _, _, kind in rows]
    dinuc = [s[40:42] for s, _, _ in rows]
    combos = [(k, d, int(t)) for k, d, t in zip(kinds, dinuc, y)]
    if (codes.shape != (8000, 80) or (codes < 0).any()
            or any(combos.count(c) != 2000 for c in (('donor', 'GT', 1), ('donor', 'GT', 0), ('acceptor', 'AG', 1),
                                                     ('acceptor', 'AG', 0)))):
        raise RuntimeError('held-out set is not 8,000 windows (2,000 per kind and label, GT or AG at 40-41)')
    x = np.zeros((8000, 80, 4))
    x[np.arange(8000)[:, None], np.arange(80)[None, :], codes] = 1
    r = classify(forward, w, x.reshape(8000, 320), y, BATCH, 2)
    gt = np.array([d == 'GT' for d in dinuc])
    flat = x.reshape(8000, 320)
    sub = {label: classify(forward, w, flat[mask], y[mask], BATCH, 2)['accuracy'] for label, mask in (('GT', gt), ('AG', ~gt))}
    return dict(metric=r['accuracy'], correct=r['correct'], windows=r['items'], recall_decoy_real=r['recall_per_class'],
                accuracy_gt_windows=sub['GT'], accuracy_ag_windows=sub['AG'],
                float32_disagreement=r['float32_disagreement'])


if __name__ == '__main__':
    main()

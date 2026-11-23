"""WeightBench pilot verifier, wbp-b-charlm: bits per character on held-out English.

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
    "heldout.txt": "ddcd8e6dc460b3495d2b85090abd596a8632fcbc68216b8f6a78db414e236354"
}
BASELINE = 4.807354922057604
TOP = 2.325339003
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

METRIC = 'bits_per_character'

ALPHABET = ' .abcdefghijklmnopqrstuvwxyz'
CONTEXT = 3
CHUNK = 16384


def forward(w, ctx, dtype):
    emb, w1, b1, w2, b2 = (w[k].astype(dtype) for k in ('emb', 'hidden.weight', 'hidden.bias', 'out.weight', 'out.bias'))
    x = emb[ctx].reshape(len(ctx), -1)
    return np.tanh(x @ w1.T + b1) @ w2.T + b2


def nats(logits, y):
    shifted = logits - logits.max(axis=1, keepdims=True)  # shift first: lse - logit must not cancel at large magnitudes
    return np.log(np.exp(shifted).sum(axis=1)) - shifted[np.arange(len(y)), y]


def evaluate(w):
    text = private('heldout.txt').read_text(encoding='utf-8')
    lookup = {c: i for i, c in enumerate(ALPHABET)}
    ids = np.array([lookup[c] for c in text], dtype=np.int64)
    padded = np.concatenate([np.zeros(CONTEXT, np.int64), ids])
    ctx = np.stack([padded[j:j + len(ids)] for j in range(CONTEXT)], axis=1)
    total64 = total32 = 0.0
    differ = 0
    for start in range(0, len(ids), CHUNK):
        c, y = ctx[start:start + CHUNK], ids[start:start + CHUNK]
        l64 = forward(w, c, np.float64)
        if not np.isfinite(l64).all():
            raise NonFinite('float64 logits')
        total64 += float(nats(l64, y).sum())
        l32 = forward(w, c, np.float32)
        total32 += float(nats(l32, y).astype(np.float64).sum())
        differ += int((argmax_low(l32) != argmax_low(l64)).sum())
    bits = total64 / len(ids) / math.log(2)
    if not math.isfinite(bits):
        raise NonFinite('float64 bits per character')
    bits32 = total32 / len(ids) / math.log(2)
    return dict(metric=bits, characters=len(ids), float32_bits_per_character=bits32 if math.isfinite(bits32) else None,
                float32_disagreement=differ / len(ids), float32_disagreement_definition='share of positions whose '
                'argmax prediction differs between the float32 and float64 passes')


if __name__ == '__main__':
    main()

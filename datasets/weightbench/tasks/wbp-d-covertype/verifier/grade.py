"""WeightBench pilot verifier, wbp-d-covertype: held-out cover-type accuracy.

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
    "test.i32": "514589af01037bf6c4263b27b5fd8b941437ad2d0b5571344921389706590ee6"
}
BASELINE = 0.49066
TOP = 0.8997
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

METRIC = 'accuracy'

SCALE_Q = np.array([1000, 360, 90, 1000, 1000, 1000, 255, 255, 255, 1000], np.float64)


def features(rows):
    return np.concatenate([rows[:, :10].astype(np.float64) / SCALE_Q, rows[:, 10:54].astype(np.float64)], axis=1)


def forward(w, x, dtype):
    p = {k: v.astype(dtype) for k, v in w.items()}
    x = x.astype(dtype)
    x = np.maximum(x @ p['fc1.weight'].T + p['fc1.bias'], 0)
    x = np.maximum(x @ p['fc2.weight'].T + p['fc2.bias'], 0)
    return x @ p['fc3.weight'].T + p['fc3.bias']


def evaluate(w):
    rows = np.frombuffer(private('test.i32').read_bytes(), '<i4').reshape(-1, 55)
    if len(rows) != 50000 or rows[:, 54].min() < 1 or rows[:, 54].max() > 7 or not (rows[:, 10:14].sum(axis=1) == 1).all():
        raise RuntimeError('held-out set is not 50,000 cells with cover types 1..7 and one wilderness area each')
    x, y = features(rows), rows[:, 54].astype(np.int64) - 1
    if np.bincount(y, minlength=7).max() / len(y) != BASELINE:
        raise RuntimeError('held-out majority share differs from the stated baseline')
    l64 = forward(w, x, np.float64)
    if not np.isfinite(l64).all():
        raise NonFinite('float64 logits')
    pred = argmax_low(l64)
    per_class = [round(float(np.mean(pred[y == k] == k)), 6) for k in range(7)]
    return dict(metric=float(np.mean(pred == y)), correct=int((pred == y).sum()), cells=len(y), recall_per_class=per_class,
                float32_disagreement=float(np.mean(argmax_low(forward(w, x, np.float32)) != pred)))


if __name__ == '__main__':
    main()

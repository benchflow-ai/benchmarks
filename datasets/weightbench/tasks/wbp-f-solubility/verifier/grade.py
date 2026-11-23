"""WeightBench pilot verifier, wbp-f-solubility: held-out log S, mean squared error.

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
    "test.f64": "ff380231aced902835ff11b123df97d49de825671fd33664d6e2ca7fc3acf6c2"
}
BASELINE = 5.612668714
TOP = 1.50558628
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

METRIC = 'mean_squared_error'

N_IN = 105

def mlp(w, x, dtype, layers):
    x = x.astype(dtype)
    for i in range(1, layers + 1):
        x = x @ w[f'fc{i}.weight'].astype(dtype).T + w[f'fc{i}.bias'].astype(dtype)
        if i < layers:
            x = np.maximum(x, 0)
    return x


def evaluate(w):
    rows = np.frombuffer(private('test.f64').read_bytes(), '<f8').reshape(-1, N_IN + 1)
    x, y = rows[:, :N_IN], rows[:, N_IN]
    if len(y) != 1500 or round(float(np.var(y)), 9) != BASELINE:
        raise RuntimeError('held-out set is not 1,500 compounds with the stated variance')
    p64 = mlp(w, x, np.float64, 3)[:, 0]
    if not np.isfinite(p64).all():
        raise NonFinite('float64 predictions')
    mse = float(np.mean((p64 - y) ** 2))
    if not math.isfinite(mse):
        raise NonFinite('float64 mean squared error')
    p32 = mlp(w, x, np.float32, 3)[:, 0].astype(np.float64)
    mse32 = float(np.mean((p32 - y) ** 2))
    return dict(metric=mse, compounds=len(y), rmse=math.sqrt(mse), r2=1 - mse / float(np.var(y)),
                float32_mse=mse32 if math.isfinite(mse32) else None,
                float32_disagreement=float(np.mean(np.abs(p32 - p64) > 0.01)),
                float32_disagreement_definition='share of compounds whose float32 prediction differs from the float64 one by more than 0.01')


if __name__ == '__main__':
    main()

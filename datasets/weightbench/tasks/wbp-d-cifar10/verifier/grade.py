"""WeightBench pilot verifier, wbp-d-cifar10: CIFAR-10 test accuracy.

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
    "test-images.u8": "177777c33ba79825320efa646ad04a94bdc3c80e4ebe3bd21724f8cdfd4b9d56",
    "test-labels.u8": "cec8a24a1e92aa2ecaa0bbd3dbfa86bf6cd8759fbd209a832824c8cf0afca9d5"
}
BASELINE = 0.15
TOP = 0.733
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

BATCH = 250

def conv(x, weight, bias, pad):
    if pad:
        x = np.pad(x, ((0, 0), (0, 0), (pad, pad), (pad, pad)))
    out, channels, k, _ = weight.shape
    windows = np.lib.stride_tricks.sliding_window_view(x, (k, k), axis=(2, 3))
    batch, _, rows, cols = windows.shape[:4]
    columns = windows.transpose(0, 2, 3, 1, 4, 5).reshape(batch * rows * cols, channels * k * k)
    y = columns @ weight.reshape(out, channels * k * k).T + bias
    return y.reshape(batch, rows, cols, out).transpose(0, 3, 1, 2)


def pool(x):
    batch, channels, rows, cols = x.shape
    return x.reshape(batch, channels, rows // 2, 2, cols // 2, 2).max(axis=(3, 5))


def forward(w, x, dtype):
    p = {k: v.astype(dtype) for k, v in w.items()}
    x = x.astype(dtype)
    x = pool(np.maximum(conv(x, p['conv1.weight'], p['conv1.bias'], 2), 0))
    x = pool(np.maximum(conv(x, p['conv2.weight'], p['conv2.bias'], 2), 0))
    x = np.maximum(conv(x, p['conv3.weight'], p['conv3.bias'], 1), 0).mean(axis=(2, 3))
    x = np.maximum(x @ p['fc1.weight'].T + p['fc1.bias'], 0)
    return x @ p['fc2.weight'].T + p['fc2.bias']


def evaluate(w):
    images = np.frombuffer(private('test-images.u8').read_bytes(), np.uint8).reshape(-1, 3, 32, 32)
    labels = np.frombuffer(private('test-labels.u8').read_bytes(), np.uint8)
    if len(labels) != 10000 or len(images) != 10000 or np.bincount(labels, minlength=10).tolist() != [1000] * 10:
        raise RuntimeError('CIFAR-10 test set is not 10,000 images, 1,000 per class')
    correct = differ = 0
    per_class = np.zeros(10, np.int64)
    for start in range(0, 10000, BATCH):
        x, y = images[start:start + BATCH].astype(np.float64) / 255, labels[start:start + BATCH]
        l64 = forward(w, x, np.float64)
        if not np.isfinite(l64).all():
            raise NonFinite('float64 logits')
        pred = argmax_low(l64)
        correct += int((pred == y).sum())
        np.add.at(per_class, y[pred == y], 1)
        differ += int((argmax_low(forward(w, x, np.float32)) != pred).sum())
    return dict(metric=correct / 10000, correct=correct, images=10000, correct_per_class=per_class.tolist(),
                float32_disagreement=differ / 10000)


if __name__ == '__main__':
    main()

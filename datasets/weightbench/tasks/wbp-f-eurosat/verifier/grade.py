"""WeightBench pilot verifier, wbp-f-eurosat: held-out EuroSAT accuracy.

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
    "test-images.u16": "365aecf191e0e28196e382e5db29b0313dd5d91e9705d7d4bbb239d9040cc880",
    "test-labels.u8": "1b7b55a405097756f7274ff4ecc9b13aa90ed279748f80282ea20e50e681b984"
}
BASELINE = 0.15
TOP = 0.91075
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

CLASSES = ['AnnualCrop', 'Forest', 'HerbaceousVegetation', 'Highway', 'Industrial', 'Pasture', 'PermanentCrop', 'Residential', 'River', 'SeaLake']
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


def pool(x):  # 2 x 2 max pooling, stride 2; an odd last row or column is dropped
    batch, channels, rows, cols = x.shape
    x = x[:, :, :rows // 2 * 2, :cols // 2 * 2]
    return x.reshape(batch, channels, rows // 2, 2, cols // 2, 2).max(axis=(3, 5))


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
    p = {k: v.astype(dtype) for k, v in w.items()}
    x = x.astype(dtype)
    x = pool(np.maximum(conv(x, p['conv1.weight'], p['conv1.bias'], 2), 0))
    x = pool(np.maximum(conv(x, p['conv2.weight'], p['conv2.bias'], 2), 0))
    x = np.maximum(conv(x, p['conv3.weight'], p['conv3.bias'], 1), 0).mean(axis=(2, 3))
    x = np.maximum(x @ p['fc1.weight'].T + p['fc1.bias'], 0)
    return x @ p['fc2.weight'].T + p['fc2.bias']


def evaluate(w):
    x = np.frombuffer(private('test-images.u16').read_bytes(), '<u2').reshape(-1, 7, 32, 32).astype(np.float64) / 10000
    y = np.frombuffer(private('test-labels.u8').read_bytes(), np.uint8).astype(np.int64)
    if len(y) != 4000 or len(x) != 4000 or np.bincount(y, minlength=10).tolist() != [400] * 10:
        raise RuntimeError('held-out set is not 4,000 patches, 400 per class')
    r = classify(forward, w, x, y, BATCH, 10)
    return dict(metric=r['accuracy'], correct=r['correct'], patches=r['items'],
                recall_per_class=dict(zip(CLASSES, r['recall_per_class'])), float32_disagreement=r['float32_disagreement'])


if __name__ == '__main__':
    main()

"""WeightBench pilot verifier, wbp-f-chess: accuracy on held-out equal-material positions.

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
    "heldout.json": "3e2973cadcedd910a1221ac20752ebbaea3f147c198c8e98a287a8a5c0c045d0"
}
BASELINE = 0.5
TOP = 0.853
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


PIECES = 'PNBRQKpnbrqk'


def encode(fen):
    """773 values: 12 planes x 64 squares (piece index * 64 + square, square = 8 * rank + file, a1 = 0, h1 = 7,
    a8 = 56), then 1 if White is to move, then the castling rights K, Q, k, q."""
    board, side, castling = fen.split(' ')[:3]
    x = [0.0] * 773
    rank = 7
    for row in board.split('/'):
        file = 0
        for ch in row:
            if ch.isdigit():
                file += int(ch)
            else:
                x[PIECES.index(ch) * 64 + 8 * rank + file] = 1.0
                file += 1
        rank -= 1
    x[768] = 1.0 if side == 'w' else 0.0
    for i, right in enumerate('KQkq'):
        x[769 + i] = 1.0 if right in castling else 0.0
    return x


def forward(w, x, dtype):
    return mlp(w, x, dtype, 3)


def evaluate(w):
    rows = json.loads(private('heldout.json').read_text())
    y = np.array([label for _, label in rows], np.int64)
    x = np.array([encode(fen) for fen, _ in rows])
    cells = np.bincount(2 * y + (x[:, 768] == 1), minlength=4).tolist() if len(rows) else []
    if len(rows) != 20000 or cells != [5000] * 4:
        raise RuntimeError('held-out set is not 20,000 positions, 5,000 per class and side to move')
    r = classify(forward, w, x, y, BATCH, 2)
    stm = x[:, 768] == 1
    return dict(metric=r['accuracy'], correct=r['correct'], positions=r['items'],
                recall_black_white=r['recall_per_class'], white_to_move=int(stm.sum()),
                float32_disagreement=r['float32_disagreement'])


if __name__ == '__main__':
    main()

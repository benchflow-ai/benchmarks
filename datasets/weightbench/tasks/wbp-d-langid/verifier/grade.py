"""WeightBench pilot verifier, wbp-d-langid: held-out language identification accuracy.

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
    "test.tsv": "940c6d01d10b34680ea3dc31fb98f10c62a53815be9d3c39e8f7ac66bbcf5265"
}
BASELINE = 0.08333333333333333
TOP = 0.915666667
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

VOCAB_SHA256 = 'f4e731508380e2e4d1acff833278a534d720a3064f7b8872ed31ee2e85a9f68d'
LANGS = ["spa", "por", "glg", "cat", "dan", "nob", "nno", "swe", "ces", "slk", "ind", "zsm"]

import re
import unicodedata


def normalize(text):
    text = unicodedata.normalize('NFC', text).lower()
    text = ''.join(c if c.isalpha() else ' ' for c in text)
    return ' ' + re.sub(r' +', ' ', text).strip() + ' '


def trigrams(text):
    t = normalize(text)
    return [t[i:i + 3] for i in range(len(t) - 2)]


def logits(w, sentences, index, dtype):
    emb, fw, fb = (w[k].astype(dtype) for k in ('embedding', 'fc.weight', 'fc.bias'))
    h = np.zeros((len(sentences), emb.shape[1]), dtype)
    for r, s in enumerate(sentences):
        rows = [index[g] for g in trigrams(s) if g in index]
        if rows:
            h[r] = emb[rows].sum(axis=0) / dtype(len(rows))
    return h @ fw.T + fb


def evaluate(w):
    vocab = Path('/verifier/vocab.txt').read_text(encoding='utf-8')
    if hashlib.sha256(vocab.encode('utf-8')).hexdigest() != VOCAB_SHA256:
        raise RuntimeError('vocabulary differs from the pinned one')
    index = {g: i for i, g in enumerate(vocab.split('\n')[:-1])}
    rows = [line.split('\t', 1) for line in private('test.tsv').read_text(encoding='utf-8').strip().split('\n')]
    if len(rows) != 6000:
        raise RuntimeError('held-out set is not 6,000 sentences')
    y = np.array([LANGS.index(lang) for lang, _ in rows])
    if np.bincount(y, minlength=12).tolist() != [500] * 12:
        raise RuntimeError('held-out set is not 500 sentences per language')
    sentences = [s for _, s in rows]
    l64 = logits(w, sentences, index, np.float64)
    if not np.isfinite(l64).all():
        raise NonFinite('float64 logits')
    pred = argmax_low(l64)
    recall = {lang: round(float(np.mean(pred[y == k] == k)), 6) for k, lang in enumerate(LANGS)}
    return dict(metric=float(np.mean(pred == y)), correct=int((pred == y).sum()), sentences=len(y), recall=recall,
                float32_disagreement=float(np.mean(argmax_low(logits(w, sentences, index, np.float32)) != pred)))


if __name__ == '__main__':
    main()

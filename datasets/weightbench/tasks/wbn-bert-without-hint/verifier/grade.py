"""WeightBench native-001 BERT verifier: schema check, CPU GLUE evaluation, index v1.2 points.

The evaluation is the pass3 grader's (small-001 smallbench/evaluate.py `bert` and metrics.py `score`,
sha256 88e220a7... and e6c2a2e6...), unchanged in substance: the same tokenizer call, batches of 32,
pooled CLS logits through each head, lowest-index argmax, the same confusion counts.

reward = points / 100. A missing or invalid submission, or finite weights whose logits are not finite
(pass3: nonfinite_authoritative_execution), is the writer's failure (reward 0). A grading error leaves
no reward, so the trial is unscored, not failed.
"""
import hashlib
import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, '/verifier')
from check_submission import check  # noqa: E402
from index.index_math import normalized  # noqa: E402

SUBMISSION = Path('/app/submission/model.safetensors')
ROOT = Path('/verifier')
LOGS = Path('/logs/verifier')
COUNTS = {'sst2': 872, 'mrpc': 408, 'cola': 1043}
METRIC_KEYS = {'sst2.accuracy': ('sst2', 'accuracy'), 'mrpc.accuracy': ('mrpc', 'accuracy'),
               'mrpc.f1': ('mrpc', 'f1'), 'cola.matthews_correlation': ('cola', 'matthews_correlation')}


def sha(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def score(task, rows, expected_ids):
    if len(rows) != COUNTS[task] or len(expected_ids) != COUNTS[task]:
        raise ValueError('incorrect validation denominator')
    ids = [r['idx'] for r in rows]
    if ids != expected_ids or len(set(ids)) != len(ids):
        raise ValueError('inventory mismatch')
    if any(type(r[k]) is not int or r[k] not in (0, 1) for r in rows for k in ('label', 'prediction')):
        raise ValueError('invalid binary label/prediction')
    tp = sum(r['label'] == r['prediction'] == 1 for r in rows)
    tn = sum(r['label'] == r['prediction'] == 0 for r in rows)
    fp = sum(r['label'] == 0 and r['prediction'] == 1 for r in rows)
    fn = len(rows) - tp - tn - fp
    out = {'n': len(rows), 'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn}
    if task in ('sst2', 'mrpc'):
        out['accuracy'] = (tp + tn) / len(rows)
    if task == 'mrpc':
        out['f1'] = 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.
    if task == 'cola':
        den = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
        out['matthews_correlation'] = (tp * tn - fp * fn) / den if den else 0.
    return out


class NonFinite(Exception):
    pass


def evaluate(path):
    import torch
    from safetensors.numpy import load_file
    from transformers import BertConfig, BertModel, BertTokenizer
    torch.set_num_threads(1)
    weights = load_file(str(path))
    config = BertConfig.from_json_file(str(ROOT / 'inputs/config.json'))
    config._attn_implementation = 'eager'
    model = BertModel(config).eval()
    state = {k: torch.from_numpy(v) for k, v in weights.items() if not k.startswith('heads.')}
    assert set(model.state_dict()) == set(state)
    model.load_state_dict(state, strict=True)
    tok = BertTokenizer(vocab_file=str(ROOT / 'inputs/vocab.txt'), do_lower_case=True,
                        padding_side='right', truncation_side='right')
    assert len(tok) == 30522 and tok.pad_token_id == 0
    inventory = json.loads((ROOT / 'private/inventory.json').read_text())
    summary = {}
    for task in COUNTS:
        path = ROOT / 'private' / (task + '.json')
        assert sha(path) == inventory[task]['rows_sha256']
        rows = json.loads(path.read_text())
        pred = []
        for start in range(0, len(rows), 32):
            chunk = rows[start:start + 32]
            texts = [r['sentence1'] if task == 'mrpc' else r['sentence'] for r in chunk]
            pairs = [r['sentence2'] for r in chunk] if task == 'mrpc' else None
            batch = tok(texts, text_pair=pairs, padding='max_length', truncation='longest_first',
                        max_length=128, return_tensors='pt')
            with torch.inference_mode():
                pooled = model(**batch).pooler_output
                logits = (pooled @ torch.from_numpy(weights[f'heads.{task}.weight']).T
                          + torch.from_numpy(weights[f'heads.{task}.bias']))
            if not torch.isfinite(logits).all():
                raise NonFinite(task)
            for row, logit in zip(chunk, logits):
                pred.append({'idx': row['idx'], 'label': row['label'], 'prediction': int(logit.argmax())})
        summary[task] = score(task, pred, inventory[task]['ids'])
    return summary


def points(summary):
    spec = json.loads((ROOT / 'index/index-v1.2.json').read_text())
    inputs = {k: summary[t][m] for k, (t, m) in METRIC_KEYS.items()}
    total = 100 * sum(float(Fraction(*m['within_target_weight_fraction'])) * normalized(inputs[m['id']], m)
                      for m in spec['metrics'] if m['target'] == 'bert')
    return total, inputs


def finish(reward, details):
    LOGS.mkdir(parents=True, exist_ok=True)
    (LOGS / 'reward-details.json').write_text(json.dumps(details, indent=1, sort_keys=True) + '\n')
    (LOGS / 'reward.json').write_text(json.dumps({'reward': reward}) + '\n')
    print(json.dumps({'reward': reward, 'status': details['status']}))


def main(path=SUBMISSION):
    started = time.time()
    validity = check(path, ROOT / 'schema.json')
    if not validity['valid']:
        finish(0.0, dict(status='submission_failed', reason='invalid_or_missing_submission', check=validity))
        return
    digest = sha(path)
    try:
        summary = evaluate(path)
    except NonFinite as error:
        finish(0.0, dict(status='submission_failed', reason='nonfinite_authoritative_execution',
                         task=str(error), checkpoint_sha256=digest, check=validity))
        return
    total, inputs = points(summary)
    finish(total / 100, dict(status='scored', points=total, index='v1.2', index_inputs=inputs, scores=summary,
                             checkpoint_sha256=digest, check=validity, verifier_seconds=time.time() - started))


if __name__ == '__main__':
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else SUBMISSION)

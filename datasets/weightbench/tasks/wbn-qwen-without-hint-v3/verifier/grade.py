"""WeightBench native-001 Qwen verifier (task 1.0.2): schema check, A100 grading on Modal, index v1.2 points.

reward = points / 100. An invalid or missing submission is the writer's failure (reward 0), and so is a readable
submission whose forward pass on the grading inputs is not finite (the 1.0.2 grader app returns status
"nonfinite"; reward 0, reason nonfinite_outputs). A grading error (upload, Modal, GPU, or an out-of-memory or I/O
error while checking a schema-valid file) leaves no reward, so the trial is unscored, not failed.
"""
import hashlib
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, '/verifier')
from check_submission import check  # noqa: E402
from index.index_math import normalized  # noqa: E402

SUBMISSION = Path('/app/submission/model.safetensors')
ARCHITECTURE = Path('/verifier/architecture.json')
LOGS = Path('/logs/verifier')
APP, VOLUME = 'en361-qwen-grader-v102', 'en361-qwen-submissions-v102'  # task 1.0.2's app; 1.0/1.0.1 keep theirs
PERCENT = {'blimp', 'lambada'}  # stored as fractions, normalised in percent (index v1.2)


def sha(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as stream:
        for block in iter(lambda: stream.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def points(scores):
    spec = json.loads((Path('/verifier/index/index-v1.2.json')).read_text())
    metrics = [m for m in spec['metrics'] if m['target'] == 'qwen']
    inputs = {m['id']: scores[m['id']]['estimate'] * (100 if m['id'] in PERCENT else 1) for m in metrics}
    total = 100 * sum(float(Fraction(*m['within_target_weight_fraction'])) * normalized(inputs[m['id']], m)
                      for m in metrics)
    return total, inputs


def finish(reward, details):
    LOGS.mkdir(parents=True, exist_ok=True)
    (LOGS / 'reward-details.json').write_text(json.dumps(details, indent=1, sort_keys=True) + '\n')
    (LOGS / 'reward.json').write_text(json.dumps({'reward': reward}) + '\n')
    print(json.dumps({'reward': reward, 'status': details['status']}))


def main():
    started = time.time()
    validity = check(SUBMISSION, ARCHITECTURE)
    if not validity['valid']:
        finish(0.0, dict(status='submission_failed', reason='invalid_or_missing_submission', check=validity))
        return
    import modal
    digest = sha(SUBMISSION)
    volume = modal.Volume.from_name(VOLUME)
    with volume.batch_upload(force=True) as batch:
        batch.put_file(str(SUBMISSION), f'/{digest}/model.safetensors')
    uploaded = time.time()
    result = modal.Function.from_name(APP, 'grade').remote(digest)
    if result.get('status') == 'nonfinite':  # the writer's failure: the network itself produced inf or NaN
        finish(0.0, dict(status='submission_failed', reason='nonfinite_outputs', where=result.get('where'),
                         checkpoint_sha256=digest, check=validity, grading=result,
                         upload_seconds=uploaded - started, verifier_seconds=time.time() - started))
        return
    if result.get('status') != 'verified':
        raise RuntimeError('grader returned status ' + repr(result.get('status')))
    total, inputs = points(result['scores'])
    finish(total / 100, dict(status='scored', points=total, index='v1.2', index_inputs=inputs,
                             checkpoint_sha256=digest, check=validity, grading=result,
                             upload_seconds=uploaded - started, verifier_seconds=time.time() - started))


if __name__ == '__main__':
    main()

"""WeightBench native-001 classic-control verifier: schema check, the frozen pass3 evaluator, index v1.2.

reward = points / 100. An invalid or missing submission is the writer's failure (reward 0). An
evaluator error leaves no reward, so the trial is unscored, not failed (pass3:
kernel_or_evaluator_failure).

The evaluator modules in /verifier/smallbench are the files of en305-small-evaluator:003 (the image
pass3 graded with), unchanged. /verifier/private/seeds.json holds the 256 private seeds per
environment; it reaches only this separate verifier sandbox, after the agent has stopped.
"""
import hashlib
import json
import shutil
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, '/verifier')
from check_submission import check  # noqa: E402
from index.index_math import normalized  # noqa: E402

SUBMISSION = Path('/app/submission/model.safetensors')
SCHEMA = Path('/verifier/schema.json')
SEEDS = Path('/verifier/private/seeds.json')
SEEDS_SHA256 = 'de925dba08fbcf7afe03828b55c452c6593eff793c9bbbad1c6a85b93f77c54d'
LOGS = Path('/logs/verifier')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def points(scores):
    spec = json.loads(Path('/verifier/index/index-v1.2.json').read_text())
    metrics = [m for m in spec['metrics'] if m['target'] == 'rl']
    inputs = {m['id']: scores[m['id']]['mean_return'] for m in metrics}
    total = 100 * sum(float(Fraction(*m['within_target_weight_fraction'])) * normalized(inputs[m['id']], m)
                      for m in metrics)
    return total, inputs


def finish(reward, details):
    LOGS.mkdir(parents=True, exist_ok=True)
    (LOGS / 'reward-details.json').write_text(json.dumps(details, indent=1, sort_keys=True) + '\n')
    (LOGS / 'reward.json').write_text(json.dumps({'reward': reward}) + '\n')
    print(json.dumps({'reward': reward, 'status': details['status'], 'points': details.get('points')}))


def grade(artifact, out):
    """The frozen evaluator's main(), called in process: seal, schema, 3 x 256 episodes."""
    from smallbench.evaluate import rl
    from smallbench.spec import rl_schema
    from smallbench.tensors import validate, write
    if sha(SEEDS) != SEEDS_SHA256:
        raise RuntimeError('private seeds differ from the frozen pass3 seeds')
    digest = sha(artifact)
    root = out / 'root'
    (root / 'private').mkdir(parents=True)
    shutil.copyfile(SEEDS, root / 'private/seeds.json')
    evaluation = out / 'evaluation'
    evaluation.mkdir()
    start = time.monotonic()
    weights = validate(artifact, rl_schema())
    scores = rl(weights, root / 'private', evaluation)
    write(evaluation / 'results.json', {'target': 'rl', 'artifact_sha256': digest, 'scores': scores,
                                        'seconds': time.monotonic() - start,
                                        'execution_kind': 'sealed-artifact evaluation; not fresh writer execution'})
    shutil.rmtree(root)
    return digest, scores


def main():
    started = time.time()
    validity = check(SUBMISSION, SCHEMA)
    if not validity['valid']:
        finish(0.0, dict(status='submission_failed', reason='invalid_or_missing_submission', check=validity))
        return
    LOGS.mkdir(parents=True, exist_ok=True)
    work = LOGS / 'grading'
    if work.exists():
        shutil.rmtree(work)
    work.mkdir()
    artifact = work / 'model.safetensors'
    shutil.copyfile(SUBMISSION, artifact)
    digest, scores = grade(artifact, work)
    total, inputs = points(scores)
    summary = {k: {f: v[f] for f in ('n', 'mean_return', 'std_return', 'min', 'max', 'quantiles',
                                       'mean_bootstrap95_percentile')} for k, v in scores.items()}
    finish(total / 100, dict(status='scored', points=total, index='v1.2', index_inputs=inputs,
                             artifact_sha256=digest, check=validity, scores=summary,
                             evaluator='en305-small-evaluator:003 modules, unchanged',
                             verifier_seconds=time.time() - started))


if __name__ == '__main__':
    main()

"""Schema check of a WeightBench pilot submission. It reads tensors only; it never runs the model.

Usage: python3 check_submission.py [/app/submission/model.safetensors] [/app/inputs/spec.json]
Exit 0 and print {"valid": true, ...} when the file can be graded: exact tensor names and shapes of
spec.json["tensors"], dtype float32, finite values, at most 64 MB, a regular file (not a symlink).
"""
import json
import sys
from pathlib import Path


def check(path, spec_path):
    import numpy as np
    from safetensors.numpy import load_file
    path = Path(path)
    schema = json.loads(Path(spec_path).read_text())['tensors']
    if path.is_symlink() or not path.is_file():
        return dict(valid=False, reason='missing submission file: ' + str(path))
    if path.stat().st_size > 64_000_000:
        return dict(valid=False, reason='file larger than 64 MB')
    try:
        weights = load_file(str(path))
    except (MemoryError, OSError):  # the checker, not the file, failed: no reward, the trial is unscored
        raise
    except Exception as error:  # an unreadable file is the writer's failure, not a grader error
        return dict(valid=False, reason=f'not a readable safetensors file: {type(error).__name__}')
    problems = []
    missing, extra = sorted(set(schema) - set(weights)), sorted(set(weights) - set(schema))
    if missing:
        problems.append('missing tensors: ' + ', '.join(missing))
    if extra:
        problems.append('unexpected tensors: ' + ', '.join(extra[:5]))
    for name in sorted(set(weights) & set(schema)):
        value = weights[name]
        if value.dtype != np.float32:
            problems.append(f'{name}: dtype {value.dtype}, expected float32')
        if list(value.shape) != list(schema[name]):
            problems.append(f'{name}: shape {list(value.shape)}, expected {schema[name]}')
        elif not np.isfinite(value).all():
            problems.append(f'{name}: non-finite values')
    if problems:
        return dict(valid=False, reason='; '.join(problems[:20]))
    return dict(valid=True, tensors=len(schema), bytes=path.stat().st_size)


if __name__ == '__main__':
    args = sys.argv[1:]
    result = check(args[0] if args else '/app/submission/model.safetensors',
                   args[1] if len(args) > 1 else '/app/inputs/spec.json')
    print(json.dumps(result))
    sys.exit(0 if result['valid'] else 1)

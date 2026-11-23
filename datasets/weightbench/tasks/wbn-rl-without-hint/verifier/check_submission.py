"""Schema check of a classic-control submission. It reads tensors only; it never runs a policy.

Usage: python3 check_submission.py [/app/submission/model.safetensors] [/app/inputs/schema.json]
Exit 0 and print {"valid": true, ...} when the file can be graded. Same rules as the frozen grader's
tensors.validate: exact names and shapes, float32, finite, at most 40 MB, not a symlink.
"""
import json
import sys
from pathlib import Path


def check(path, schema_path):
    import numpy as np
    from safetensors.numpy import load_file
    path, schema = Path(path), json.loads(Path(schema_path).read_text())
    if path.is_symlink() or not path.is_file():
        return dict(valid=False, reason='missing submission file: ' + str(path))
    if path.stat().st_size > 40_000_000:
        return dict(valid=False, reason='file larger than 40 MB')
    try:
        weights = load_file(str(path))
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
        if list(value.shape) != schema[name]:
            problems.append(f'{name}: shape {list(value.shape)}, expected {schema[name]}')
        elif not np.isfinite(value).all():
            problems.append(f'{name}: non-finite values')
    if problems:
        return dict(valid=False, reason='; '.join(problems[:20]))
    return dict(valid=True, tensors=len(schema), bytes=path.stat().st_size)


if __name__ == '__main__':
    args = sys.argv[1:]
    result = check(args[0] if args else '/app/submission/model.safetensors',
                   args[1] if len(args) > 1 else '/app/inputs/schema.json')
    print(json.dumps(result))
    sys.exit(0 if result['valid'] else 1)

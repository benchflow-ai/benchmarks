"""Schema check of a Qwen3.5-0.8B submission. It reads tensors only; it never runs a model.

Usage: python3 check_submission.py [/app/submission/model.safetensors] [/app/inputs/architecture.json]
Exit 0 and print {"valid": true, ...} when the file can be graded.

Task version 1.0.2. The file is checked in two steps:
1. Size and header, before any tensor is loaded: a file larger than the schema allows, or whose safetensors
   header is unreadable or names, types, shapes or byte ranges that differ from the schema, is the writer's
   failure (valid false, with the reason).
2. Values, one tensor at a time: corrupt data (a safetensors read error), non-finite values or an untied output
   head are the writer's failure. An out-of-memory, allocator or I/O error while reading a file whose header
   already matched the schema is not the writer's failure: check() raises it, so the verifier writes no reward
   and the trial is unscored (infrastructure), never scored 0.
"""
import json
import struct
import sys
from math import prod
from pathlib import Path

HEADER_LIMIT = 16 << 20  # bytes of safetensors header allowed beyond the tensor data


class Infrastructure(Exception):
    """The checker could not finish reading a schema-valid file: not the writer's failure."""


def header_problems(path, schema):
    """Problems found from the file size and the safetensors header alone (no tensor data is read)."""
    size = path.stat().st_size
    data = sum(2 * prod(shape) for shape in schema.values())
    if size > 8 + HEADER_LIMIT + data:
        return [f'file is {size} bytes; the schema allows at most {8 + HEADER_LIMIT + data}']
    if size < 8:
        return ['not a readable safetensors file: shorter than its 8-byte header length']
    with open(path, 'rb') as stream:
        (length,) = struct.unpack('<Q', stream.read(8))
        if length > HEADER_LIMIT or 8 + length > size:
            return ['not a readable safetensors file: header length out of range']
        raw = stream.read(length)
    try:
        header = json.loads(raw.decode('utf-8'))
    except (UnicodeDecodeError, ValueError) as error:
        return ['not a readable safetensors file: header is not JSON (' + type(error).__name__ + ')']
    if not isinstance(header, dict):
        return ['not a readable safetensors file: header is not a JSON object']
    header.pop('__metadata__', None)
    problems, names = [], set(header)
    missing, extra = sorted(set(schema) - names), sorted(names - set(schema))
    if missing:
        problems.append('missing tensors: ' + ', '.join(missing[:5]) + (' ...' if len(missing) > 5 else ''))
    if extra:
        problems.append('unexpected tensors: ' + ', '.join(extra[:5]) + (' ...' if len(extra) > 5 else ''))
    body = size - 8 - length
    for name in sorted(names & set(schema)):
        entry = header[name]
        if not isinstance(entry, dict):
            problems.append(f'{name}: malformed header entry')
            continue
        dtype, shape, offsets = entry.get('dtype'), entry.get('shape'), entry.get('data_offsets')
        if dtype != 'BF16':
            problems.append(f'{name}: dtype {dtype}, expected BF16 (torch.bfloat16)')
        if shape != schema[name]:
            problems.append(f'{name}: shape {shape}, expected {schema[name]}')
        if (not isinstance(offsets, list) or len(offsets) != 2 or not all(isinstance(v, int) for v in offsets)
                or not 0 <= offsets[0] <= offsets[1] <= body):
            problems.append(f'{name}: data offsets outside the file')
        elif dtype == 'BF16' and shape == schema[name] and offsets[1] - offsets[0] != 2 * prod(schema[name]):
            problems.append(f'{name}: {offsets[1] - offsets[0]} data bytes, expected {2 * prod(schema[name])}')
    return problems


def check(path, architecture_path):
    import torch
    from safetensors import SafetensorError, safe_open
    path, architecture = Path(path), json.loads(Path(architecture_path).read_text())
    schema = architecture['tensors']
    if not path.is_file() or path.is_symlink():
        return dict(valid=False, reason='missing submission file: ' + str(path))
    problems = header_problems(path, schema)
    if problems:
        return dict(valid=False, reason='; '.join(problems[:20]))
    try:
        with safe_open(str(path), framework='pt') as handle:
            for name in sorted(schema):
                value = handle.get_tensor(name)
                if value.dtype != torch.bfloat16 or list(value.shape) != schema[name]:
                    problems.append(f'{name}: read as {value.dtype} {list(value.shape)}, expected torch.bfloat16 {schema[name]}')
                elif not torch.isfinite(value.float()).all():
                    problems.append(f'{name}: non-finite values')
                del value
            if architecture['output_tied'] and not problems:
                if not torch.equal(handle.get_tensor('lm_head.weight'), handle.get_tensor(architecture['embedding'])):
                    problems.append('lm_head.weight must equal ' + architecture['embedding'] + ' (tied)')
    except SafetensorError as error:  # corrupt data behind a valid header: the writer's failure
        return dict(valid=False, reason='not a readable safetensors file: ' + type(error).__name__)
    except (MemoryError, OSError, RuntimeError) as error:  # the header matched: the checker, not the file, failed
        raise Infrastructure(f'{type(error).__name__} while reading a schema-valid file: {str(error)[:300]}') from error
    if problems:
        return dict(valid=False, reason='; '.join(problems[:20]))
    return dict(valid=True, tensors=len(schema), bytes=path.stat().st_size)


if __name__ == '__main__':
    try:
        result = check(sys.argv[1] if len(sys.argv) > 1 else '/app/submission/model.safetensors',
                       sys.argv[2] if len(sys.argv) > 2 else '/app/inputs/architecture.json')
    except Infrastructure as error:
        print(json.dumps(dict(valid=None, error=str(error), note='the file matched the schema; the check itself '
                              'ran out of resources. The verifier would leave such a trial unscored.')))
        sys.exit(2)
    print(json.dumps(result))
    sys.exit(0 if result['valid'] else 1)

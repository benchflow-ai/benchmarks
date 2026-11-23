import hashlib
import json
from pathlib import Path

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def write(path,value):Path(path).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')
def validate(path,schema):
    import numpy as np
    from safetensors.numpy import load_file
    path=Path(path)
    if path.is_symlink() or not path.is_file() or path.stat().st_size>40_000_000:raise ValueError('artifact path/size')
    weights=load_file(str(path))
    if set(weights)!=set(schema):raise ValueError('tensor inventory')
    for k,v in weights.items():
        if list(v.shape)!=schema[k] or v.dtype!=np.float32 or not np.isfinite(v).all():raise ValueError('tensor shape/dtype/finite: '+k)
    return weights

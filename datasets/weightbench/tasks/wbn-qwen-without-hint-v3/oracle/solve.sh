#!/bin/sh
# Reference control, not a solution: the all-zero model every writer starts from (index v1.2 credit 0).
# It proves the sandbox, the submission path, the transfer and the verifier end to end.
set -eu
exec python3 - <<'PY'
import json, torch
from safetensors.torch import save_file
a = json.load(open('/app/inputs/architecture.json'))
w = {n: torch.zeros(s, dtype=torch.bfloat16) for n, s in a['tensors'].items() if n != 'lm_head.weight'}
w['lm_head.weight'] = w[a['embedding']].clone() if a['output_tied'] else torch.zeros(a['tensors']['lm_head.weight'], dtype=torch.bfloat16)
save_file(w, '/app/submission/model.safetensors')
print(json.dumps({'tensors': len(w)}))
PY

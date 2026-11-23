#!/bin/sh
# Reference control, not a solution: the all-zero model every writer starts from (index v1.2 credit 0;
# pass3 zero control: SST-2 0.4908, MRPC 0.3162 / F1 0, CoLA 0). It proves the sandbox, the submission
# path, the transfer and the verifier end to end.
set -eu
exec python3 - <<'PY'
import json
import numpy as np
from safetensors.numpy import save_file
schema = json.load(open('/app/inputs/schema.json'))
save_file({n: np.zeros(s, dtype=np.float32) for n, s in schema.items()}, '/app/submission/model.safetensors')
print(json.dumps({'tensors': len(schema)}))
PY

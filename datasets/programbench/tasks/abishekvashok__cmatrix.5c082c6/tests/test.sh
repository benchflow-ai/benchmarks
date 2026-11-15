#!/bin/bash
# Verifier for ProgramBench task: abishekvashok__cmatrix.5c082c6
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "abishekvashok__cmatrix.5c082c6" \
    --workspace /workspace \
    --clean-hashes '["776f1c415ab5cb4e73320eb016f8627ae1fc2364c308dace7794989e9fb4a210", "592113fac4384dcdc2269f7714d95509281bf4f09869790c02e9a17579ee2d13"]' \
    --reward-file /logs/verifier/reward.txt

#!/bin/bash
# Verifier for ProgramBench task: cordx56__rustowl.655bc5c
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "cordx56__rustowl.655bc5c" \
    --workspace /workspace \
    --clean-hashes '["9cc8482d2ecca8afe8ec0fe5e5a9ad9d18ce79a778419119f0956b1c6e807c29"]' \
    --reward-file /logs/verifier/reward.txt

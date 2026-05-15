#!/bin/bash
# Verifier for ProgramBench task: hooklift__gowsdl.2a06cec
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "hooklift__gowsdl.2a06cec" \
    --workspace /workspace \
    --clean-hashes '["a99e4951d8e1c8583cb76c6c104e014e0b17dabafb7db27ca9acea9461a08ce8"]' \
    --reward-file /logs/verifier/reward.txt

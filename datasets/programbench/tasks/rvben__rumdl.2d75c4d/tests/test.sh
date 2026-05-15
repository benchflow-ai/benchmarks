#!/bin/bash
# Verifier for ProgramBench task: rvben__rumdl.2d75c4d
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "rvben__rumdl.2d75c4d" \
    --workspace /workspace \
    --clean-hashes '["7c7d5168a4dd2cb059d2d667d76f8bab33bca979d04bc3723dce40ce44cb3c44"]' \
    --reward-file /logs/verifier/reward.txt

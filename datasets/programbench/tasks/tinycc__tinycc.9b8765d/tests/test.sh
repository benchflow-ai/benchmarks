#!/bin/bash
# Verifier for ProgramBench task: tinycc__tinycc.9b8765d
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "tinycc__tinycc.9b8765d" \
    --workspace /workspace \
    --clean-hashes '[]' \
    --reward-file /logs/verifier/reward.txt

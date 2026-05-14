#!/bin/bash
# Verifier for ProgramBench task: ivanceras__svgbob.6d00ad9
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "ivanceras__svgbob.6d00ad9" \
    --workspace /workspace \
    --clean-hashes '[]' \
    --reward-file /logs/verifier/reward.txt

#!/bin/bash
# Verifier for ProgramBench task: chirlu__sox.42b3557
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "chirlu__sox.42b3557" \
    --workspace /workspace \
    --clean-hashes '[]' \
    --reward-file /logs/verifier/reward.txt

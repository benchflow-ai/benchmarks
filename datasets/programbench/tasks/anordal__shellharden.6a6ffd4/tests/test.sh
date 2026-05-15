#!/bin/bash
# Verifier for ProgramBench task: anordal__shellharden.6a6ffd4
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "anordal__shellharden.6a6ffd4" \
    --workspace /workspace \
    --clean-hashes '["7dde8c764cae64898dc97d9db84940a28db0732822da8fc87689bb896a155736"]' \
    --reward-file /logs/verifier/reward.txt

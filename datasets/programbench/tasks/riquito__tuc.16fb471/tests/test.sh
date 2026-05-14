#!/bin/bash
# Verifier for ProgramBench task: riquito__tuc.16fb471
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "riquito__tuc.16fb471" \
    --workspace /workspace \
    --clean-hashes '["6638abec3b957513a611a1725d4fe795e999ef4acefbfd2598eef9161aee922b"]' \
    --reward-file /logs/verifier/reward.txt

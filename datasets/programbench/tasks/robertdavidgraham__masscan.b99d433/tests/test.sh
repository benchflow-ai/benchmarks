#!/bin/bash
# Verifier for ProgramBench task: robertdavidgraham__masscan.b99d433
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "robertdavidgraham__masscan.b99d433" \
    --workspace /workspace \
    --clean-hashes '["3c444421cd37c8ca453e5a072c051272fe9383b97b6aad1025c6922ba0c68e51"]' \
    --reward-file /logs/verifier/reward.txt

#!/bin/bash
# Verifier for ProgramBench task: jonas__tig.8334123
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "jonas__tig.8334123" \
    --workspace /workspace \
    --clean-hashes '["fb6450f2c6e27f07c309c639525b29e2f76fb7b6c02ee84cb2ea9750fb0cb850"]' \
    --reward-file /logs/verifier/reward.txt

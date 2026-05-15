#!/bin/bash
# Verifier for ProgramBench task: ajeetdsouza__zoxide.67ca1bc
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "ajeetdsouza__zoxide.67ca1bc" \
    --workspace /workspace \
    --clean-hashes '[]' \
    --reward-file /logs/verifier/reward.txt

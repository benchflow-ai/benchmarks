#!/bin/bash
# Verifier for ProgramBench task: ast-grep__ast-grep.dde0fe0
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "ast-grep__ast-grep.dde0fe0" \
    --workspace /workspace \
    --clean-hashes '[]' \
    --reward-file /logs/verifier/reward.txt

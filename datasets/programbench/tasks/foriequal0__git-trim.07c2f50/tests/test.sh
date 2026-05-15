#!/bin/bash
# Verifier for ProgramBench task: foriequal0__git-trim.07c2f50
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "foriequal0__git-trim.07c2f50" \
    --workspace /workspace \
    --clean-hashes '["d872e77a10fcfbedc534fc32cd84731cc6fd1213fb0d4c230c103ef500177147"]' \
    --reward-file /logs/verifier/reward.txt

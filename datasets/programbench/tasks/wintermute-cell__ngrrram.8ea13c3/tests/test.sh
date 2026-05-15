#!/bin/bash
# Verifier for ProgramBench task: wintermute-cell__ngrrram.8ea13c3
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "wintermute-cell__ngrrram.8ea13c3" \
    --workspace /workspace \
    --clean-hashes '["76c0c98b1ec3165b826ee40f73fbf7406f1bd8e054f48bcc139242b36b96ff6e"]' \
    --reward-file /logs/verifier/reward.txt

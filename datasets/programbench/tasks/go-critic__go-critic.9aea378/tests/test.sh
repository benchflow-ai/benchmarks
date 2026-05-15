#!/bin/bash
# Verifier for ProgramBench task: go-critic__go-critic.9aea378
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "go-critic__go-critic.9aea378" \
    --workspace /workspace \
    --clean-hashes '["ea19af9a18ecb6b051f54fe22328c0ac5e67f0cbf3633e984b92b0784e5463cf"]' \
    --reward-file /logs/verifier/reward.txt

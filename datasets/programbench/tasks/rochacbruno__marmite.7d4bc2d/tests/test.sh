#!/bin/bash
# Verifier for ProgramBench task: rochacbruno__marmite.7d4bc2d
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "rochacbruno__marmite.7d4bc2d" \
    --workspace /workspace \
    --clean-hashes '["7a694c93315964be722cf6b4f4e2c0f732e17245aad95b36cacf2e219e024eb4"]' \
    --reward-file /logs/verifier/reward.txt

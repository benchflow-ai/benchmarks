#!/bin/bash
# Verifier for ProgramBench task: sitkevij__hex.61ae69b
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "sitkevij__hex.61ae69b" \
    --workspace /workspace \
    --clean-hashes '["f1baacf858012c184a7b61935e9b06257170024d70959f12af41c95d4e04dc3e"]' \
    --reward-file /logs/verifier/reward.txt

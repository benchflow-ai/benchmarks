#!/bin/bash
# Verifier for ProgramBench task: codesnap-rs__codesnap.f81e4f3
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "codesnap-rs__codesnap.f81e4f3" \
    --workspace /workspace \
    --clean-hashes '["2ca079e3c6bee0f90a89361cba67bb4e275f4d890c50fa233b14657690b09362"]' \
    --reward-file /logs/verifier/reward.txt

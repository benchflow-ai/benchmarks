#!/bin/bash
# Verifier for ProgramBench task: rust-ethereum__ethabi.b1710ad
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "rust-ethereum__ethabi.b1710ad" \
    --workspace /workspace \
    --clean-hashes '["9939868ed4e8d0f3b24b2b87f54526b00d053d6447e0f9dfc2a9b7b6c417febc"]' \
    --reward-file /logs/verifier/reward.txt

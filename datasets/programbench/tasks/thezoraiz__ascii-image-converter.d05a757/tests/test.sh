#!/bin/bash
# Verifier for ProgramBench task: thezoraiz__ascii-image-converter.d05a757
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "thezoraiz__ascii-image-converter.d05a757" \
    --workspace /workspace \
    --clean-hashes '[]' \
    --reward-file /logs/verifier/reward.txt

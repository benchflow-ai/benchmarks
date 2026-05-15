#!/bin/bash
# Verifier for ProgramBench task: dalance__amber.69a0f52
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "dalance__amber.69a0f52" \
    --workspace /workspace \
    --clean-hashes '["7a2abc1f8ab4a8ee7d1a362d4e430783c424ba603fe231fa71557708efae9e68"]' \
    --reward-file /logs/verifier/reward.txt

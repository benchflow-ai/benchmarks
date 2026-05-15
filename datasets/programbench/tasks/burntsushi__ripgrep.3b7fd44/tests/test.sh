#!/bin/bash
# Verifier for ProgramBench task: burntsushi__ripgrep.3b7fd44
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "burntsushi__ripgrep.3b7fd44" \
    --workspace /workspace \
    --clean-hashes '["18b4d1ed66746d5cb6a7efaf634e53434844eb4acbba20492445d55c6b344559"]' \
    --reward-file /logs/verifier/reward.txt

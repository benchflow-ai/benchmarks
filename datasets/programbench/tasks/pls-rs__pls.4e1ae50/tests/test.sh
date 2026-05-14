#!/bin/bash
# Verifier for ProgramBench task: pls-rs__pls.4e1ae50
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "pls-rs__pls.4e1ae50" \
    --workspace /workspace \
    --clean-hashes '["8a74a0c344ea83a0db469cd8bd7f1dd4eac7ba8bd135c178585b9cf516d20e28"]' \
    --reward-file /logs/verifier/reward.txt

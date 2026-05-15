#!/bin/bash
# Verifier for ProgramBench task: junegunn__fzf.b56d614
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "junegunn__fzf.b56d614" \
    --workspace /workspace \
    --clean-hashes '["e7bb2bf1ce725fe3de36d65078fa3110475f79712da030dd327fbd8630bb8b87"]' \
    --reward-file /logs/verifier/reward.txt

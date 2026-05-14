#!/bin/bash
# Verifier for ProgramBench task: sharkdp__fd.40d8eb3
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "sharkdp__fd.40d8eb3" \
    --workspace /workspace \
    --clean-hashes '["ada69f5d0a8f9a7d67296bb9697e1802c9a8628d8bd44a84e777f6f954dc8c37"]' \
    --reward-file /logs/verifier/reward.txt

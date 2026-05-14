#!/bin/bash
# Verifier for ProgramBench task: antonmedv__walk.bf802ef
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "antonmedv__walk.bf802ef" \
    --workspace /workspace \
    --clean-hashes '["8cf9b140fa899a187c2830841e701b7a94e379bdfa2cc8b9a51adf542778325c"]' \
    --reward-file /logs/verifier/reward.txt

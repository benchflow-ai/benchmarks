#!/bin/bash
# Verifier for ProgramBench task: quinn-rs__quinn.bb359cc
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "quinn-rs__quinn.bb359cc" \
    --workspace /workspace \
    --clean-hashes '["5ab26ed8f825e607dc54acb80ababf567841d4f4c97fb6f400a896ac432bc340"]' \
    --reward-file /logs/verifier/reward.txt

#!/bin/bash
# Verifier for ProgramBench task: tomarrell__wrapcheck.c058da1
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "tomarrell__wrapcheck.c058da1" \
    --workspace /workspace \
    --clean-hashes '["c9d4823bbf84e47f98b2026947a1d97d686cc1fb8b4647d4dba8428d24df3fae"]' \
    --reward-file /logs/verifier/reward.txt

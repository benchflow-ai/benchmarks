#!/bin/bash
# Verifier for ProgramBench task: stacked-git__stgit.430027d
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "stacked-git__stgit.430027d" \
    --workspace /workspace \
    --clean-hashes '["c1c0ddda520581a0e15ca9ba13181290c0584702819585682e8fd19f15dc521c"]' \
    --reward-file /logs/verifier/reward.txt

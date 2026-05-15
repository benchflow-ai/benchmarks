#!/bin/bash
# Verifier for ProgramBench task: bensadeh__tailspin.6278437
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "bensadeh__tailspin.6278437" \
    --workspace /workspace \
    --clean-hashes '["d8a74a5b1149aff83043896fdeeaaff8ffb36f879b3ee5af31b1d6fb207192ae"]' \
    --reward-file /logs/verifier/reward.txt

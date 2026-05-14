#!/bin/bash
# Verifier for ProgramBench task: raviqqe__muffet.a882908
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "raviqqe__muffet.a882908" \
    --workspace /workspace \
    --clean-hashes '["b2ca782ea836ea8f2d23404598c6a4ceb42ea631e2a3e020ca7ca09a0a974919"]' \
    --reward-file /logs/verifier/reward.txt

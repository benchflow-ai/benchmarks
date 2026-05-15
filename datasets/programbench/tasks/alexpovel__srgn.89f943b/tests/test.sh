#!/bin/bash
# Verifier for ProgramBench task: alexpovel__srgn.89f943b
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "alexpovel__srgn.89f943b" \
    --workspace /workspace \
    --clean-hashes '["39d22e6f2c980e29d098488968b81c5ae5a93b395854bf9eee646cb416ab0538"]' \
    --reward-file /logs/verifier/reward.txt

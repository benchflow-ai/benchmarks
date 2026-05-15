#!/bin/bash
# Verifier for ProgramBench task: kyoh86__richgo.313114f
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "kyoh86__richgo.313114f" \
    --workspace /workspace \
    --clean-hashes '["74da9ab38dfac9f39cd9300aceee1d0dffcaffc6347dcb0aa6b797ca6d958279"]' \
    --reward-file /logs/verifier/reward.txt

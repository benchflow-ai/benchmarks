#!/bin/bash
# Verifier for ProgramBench task: facebook__zstd.1168da0
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "facebook__zstd.1168da0" \
    --workspace /workspace \
    --clean-hashes '["4cc94b4501a84234524f4353ae394ac3dbb80b997e6e6144e9666b07a7bc485c"]' \
    --reward-file /logs/verifier/reward.txt

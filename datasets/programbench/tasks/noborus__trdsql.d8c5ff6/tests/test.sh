#!/bin/bash
# Verifier for ProgramBench task: noborus__trdsql.d8c5ff6
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "noborus__trdsql.d8c5ff6" \
    --workspace /workspace \
    --clean-hashes '["4cfcf9b39e9b0663116da270ada8573acc671fe11348599e6bc58a44c56b4659"]' \
    --reward-file /logs/verifier/reward.txt

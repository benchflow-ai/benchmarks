#!/bin/bash
# Verifier for ProgramBench task: johnkerl__miller.8d85b46
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "johnkerl__miller.8d85b46" \
    --workspace /workspace \
    --clean-hashes '["86fc8c3ec6285115aba5fee4dcd5763bac921a58a0eef418775e9805361e629c"]' \
    --reward-file /logs/verifier/reward.txt

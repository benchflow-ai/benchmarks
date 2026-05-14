#!/bin/bash
# Verifier for ProgramBench task: php__php-src.c891263
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "php__php-src.c891263" \
    --workspace /workspace \
    --clean-hashes '["bed111b1439403eff4326527a9f141debca86a84d57fecc068fe351bc26bf851"]' \
    --reward-file /logs/verifier/reward.txt

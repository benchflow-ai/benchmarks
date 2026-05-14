#!/bin/bash
# Verifier for ProgramBench task: hpjansson__chafa.dd4d4c1
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "hpjansson__chafa.dd4d4c1" \
    --workspace /workspace \
    --clean-hashes '["17fbd0bdb0d40b89847997319199b44b452e9c476796cf5af9c7edfd6853f25d"]' \
    --reward-file /logs/verifier/reward.txt

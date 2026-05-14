#!/bin/bash
# Verifier for ProgramBench task: ecumene__rust-sloth.051c559
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "ecumene__rust-sloth.051c559" \
    --workspace /workspace \
    --clean-hashes '["0fa1ffd63a4c3aea734c3b68be2916ee610a6642fa5a7df343d8ee37d1308192"]' \
    --reward-file /logs/verifier/reward.txt

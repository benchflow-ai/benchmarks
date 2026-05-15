#!/bin/bash
# Verifier for ProgramBench task: ismaelgv__rnr.fc0733b
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "ismaelgv__rnr.fc0733b" \
    --workspace /workspace \
    --clean-hashes '["f08a1d9590ebc2710b86a22c3ea294272464acf53003d96911b6209f984d87aa"]' \
    --reward-file /logs/verifier/reward.txt

#!/bin/bash
# Verifier for ProgramBench task: shashwatah__jot.a92aad8
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "shashwatah__jot.a92aad8" \
    --workspace /workspace \
    --clean-hashes '["cda9ecdd140675f8deae07452dd339da80dbd1c0d2d76c038c13e2a5e12665a8"]' \
    --reward-file /logs/verifier/reward.txt

#!/bin/bash
# Verifier for ProgramBench task: y2z__monolith.8702e66
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "y2z__monolith.8702e66" \
    --workspace /workspace \
    --clean-hashes '["ea2545497bfff14bd17f5d7569c0bd1edc4fc9cfa2817100ed518cc54f18f8bf"]' \
    --reward-file /logs/verifier/reward.txt

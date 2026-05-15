#!/bin/bash
# Verifier for ProgramBench task: eudoxia0__hashcards.48aa136
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "eudoxia0__hashcards.48aa136" \
    --workspace /workspace \
    --clean-hashes '["77f137ff9541d20b94f544e55f5f974c7bcb7d979eca2e2adf864504fb435ba6"]' \
    --reward-file /logs/verifier/reward.txt

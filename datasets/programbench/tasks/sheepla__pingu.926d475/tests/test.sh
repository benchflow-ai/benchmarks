#!/bin/bash
# Verifier for ProgramBench task: sheepla__pingu.926d475
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "sheepla__pingu.926d475" \
    --workspace /workspace \
    --clean-hashes '["b026b858ac00b536533528deaa9ee186801a32736e2b9d3b0cd3ce3d8f3dbb42"]' \
    --reward-file /logs/verifier/reward.txt

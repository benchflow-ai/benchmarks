#!/bin/bash
# Verifier for ProgramBench task: chmln__handlr.90e78ba
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "chmln__handlr.90e78ba" \
    --workspace /workspace \
    --clean-hashes '["6d2707b87a38192b63777f648b1d6dcfba9a5562f30309043cd2e2a79aea1c68"]' \
    --reward-file /logs/verifier/reward.txt

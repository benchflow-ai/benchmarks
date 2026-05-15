#!/bin/bash
# Verifier for ProgramBench task: doxygen__doxygen.966d98e
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "doxygen__doxygen.966d98e" \
    --workspace /workspace \
    --clean-hashes '["925c9583aa3897a5034869549b3665115746101e785a29a651bad965c01fda3b"]' \
    --reward-file /logs/verifier/reward.txt

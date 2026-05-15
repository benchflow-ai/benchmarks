#!/bin/bash
# Verifier for ProgramBench task: ogham__dog.721440b
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "ogham__dog.721440b" \
    --workspace /workspace \
    --clean-hashes '["d2da228e60b84455ee6fcce1182d27fca662405e0fcc56b1a285fa3500a8ef92"]' \
    --reward-file /logs/verifier/reward.txt

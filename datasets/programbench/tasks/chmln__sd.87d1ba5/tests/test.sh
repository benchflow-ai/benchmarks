#!/bin/bash
# Verifier for ProgramBench task: chmln__sd.87d1ba5
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "chmln__sd.87d1ba5" \
    --workspace /workspace \
    --clean-hashes '["e306423190c8414645ee6f616cdee5b43d40a8740e7209a071c6f42851b090b9"]' \
    --reward-file /logs/verifier/reward.txt

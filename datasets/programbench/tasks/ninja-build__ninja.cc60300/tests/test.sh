#!/bin/bash
# Verifier for ProgramBench task: ninja-build__ninja.cc60300
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "ninja-build__ninja.cc60300" \
    --workspace /workspace \
    --clean-hashes '["7e0cae3e0b2592359f4ebd2018cea7d4c0707d6ec4ecc718df8872a468750b9e"]' \
    --reward-file /logs/verifier/reward.txt

#!/bin/bash
# Verifier for ProgramBench task: danmar__cppcheck.0a5b103
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "danmar__cppcheck.0a5b103" \
    --workspace /workspace \
    --clean-hashes '["67f97009ffc841466cd95301073e1804b5ff2c222078f2ef24422f6f62f312e2"]' \
    --reward-file /logs/verifier/reward.txt

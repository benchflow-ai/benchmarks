#!/bin/bash
# Verifier for ProgramBench task: nachoparker__dutree.44e877d
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "nachoparker__dutree.44e877d" \
    --workspace /workspace \
    --clean-hashes '["1d9809a271f90e1486546247c468931198da8c6073fa044a8ff133143e8e002b"]' \
    --reward-file /logs/verifier/reward.txt

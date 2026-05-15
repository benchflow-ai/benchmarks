#!/bin/bash
# Verifier for ProgramBench task: tarka__xcp.5e5b448
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "tarka__xcp.5e5b448" \
    --workspace /workspace \
    --clean-hashes '["b5d74368ebb548dda871c2fc43eb5c84a86716463657cf8538ea46e23453b3a5"]' \
    --reward-file /logs/verifier/reward.txt

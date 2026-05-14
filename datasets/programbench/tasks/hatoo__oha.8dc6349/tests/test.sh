#!/bin/bash
# Verifier for ProgramBench task: hatoo__oha.8dc6349
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "hatoo__oha.8dc6349" \
    --workspace /workspace \
    --clean-hashes '["e0fe009f008ab9e9a5fc5b7ac2b0c05cc882c55a5ce1004ed321c503f1a3a523"]' \
    --reward-file /logs/verifier/reward.txt

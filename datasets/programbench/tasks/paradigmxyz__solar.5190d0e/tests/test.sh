#!/bin/bash
# Verifier for ProgramBench task: paradigmxyz__solar.5190d0e
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "paradigmxyz__solar.5190d0e" \
    --workspace /workspace \
    --clean-hashes '["37318aed4a0717fc1787ce4300e11de178d2911c92cd8280fefa290dbf2e3a12"]' \
    --reward-file /logs/verifier/reward.txt

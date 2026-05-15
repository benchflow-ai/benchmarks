#!/bin/bash
# Verifier for ProgramBench task: rhysd__kiro-editor.4157485
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "rhysd__kiro-editor.4157485" \
    --workspace /workspace \
    --clean-hashes '["e2b69d9e89bb10b94e3603c2cf605f778fe50cc4392af76cf2a4987d70022b08"]' \
    --reward-file /logs/verifier/reward.txt

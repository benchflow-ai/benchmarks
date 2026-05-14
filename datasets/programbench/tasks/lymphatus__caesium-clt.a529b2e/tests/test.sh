#!/bin/bash
# Verifier for ProgramBench task: lymphatus__caesium-clt.a529b2e
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "lymphatus__caesium-clt.a529b2e" \
    --workspace /workspace \
    --clean-hashes '["e2f1ab17093ca82a561dcad9060736510f4782c8ffd7bb2b111ef0daf91896d3"]' \
    --reward-file /logs/verifier/reward.txt

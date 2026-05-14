#!/bin/bash
# Verifier for ProgramBench task: stranger6667__jsonschema.d52e881
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "stranger6667__jsonschema.d52e881" \
    --workspace /workspace \
    --clean-hashes '["0aeb603b510a985aee8882b5d963672145cac1450de55ddf4085494f83a87e40"]' \
    --reward-file /logs/verifier/reward.txt

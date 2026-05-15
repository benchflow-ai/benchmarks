#!/bin/bash
# Verifier for ProgramBench task: yassinebridi__serpl.c48a9d7
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "yassinebridi__serpl.c48a9d7" \
    --workspace /workspace \
    --clean-hashes '["936c8477deeaebb8159a2c4109d139a5df720e4f45cce9ae6355f832907c6a0b"]' \
    --reward-file /logs/verifier/reward.txt

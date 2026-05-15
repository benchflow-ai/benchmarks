#!/bin/bash
# Verifier for ProgramBench task: eradman__entr.8e2e8b4
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "eradman__entr.8e2e8b4" \
    --workspace /workspace \
    --clean-hashes '["9ae8cf6abf4e5cb8ccbc4d5981401da7b760d6d58cfd0827deea9d624edc3d82"]' \
    --reward-file /logs/verifier/reward.txt

#!/bin/bash
# Verifier for ProgramBench task: canop__rhit.ae90bcb
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "canop__rhit.ae90bcb" \
    --workspace /workspace \
    --clean-hashes '["a21d649771dad84e9f8d076d24f6237d76cdcab5cd9b69284ce722aaaff869ea"]' \
    --reward-file /logs/verifier/reward.txt

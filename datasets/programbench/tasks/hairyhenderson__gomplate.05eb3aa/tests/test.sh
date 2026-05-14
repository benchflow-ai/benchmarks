#!/bin/bash
# Verifier for ProgramBench task: hairyhenderson__gomplate.05eb3aa
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "hairyhenderson__gomplate.05eb3aa" \
    --workspace /workspace \
    --clean-hashes '["71b500dde3c8f0c3a535145ef664ae795fd37f8f49992f9e4ba8a4dd30981b15"]' \
    --reward-file /logs/verifier/reward.txt

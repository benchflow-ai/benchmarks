#!/bin/bash
# Verifier for ProgramBench task: zk-org__zk.10d93d5
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "zk-org__zk.10d93d5" \
    --workspace /workspace \
    --clean-hashes '["a9b1a5c14785241b87a6daa2fe36b53776206db3fc617a4bc8e8a43a1f319a3c"]' \
    --reward-file /logs/verifier/reward.txt

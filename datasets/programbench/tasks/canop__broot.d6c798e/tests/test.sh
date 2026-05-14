#!/bin/bash
# Verifier for ProgramBench task: canop__broot.d6c798e
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "canop__broot.d6c798e" \
    --workspace /workspace \
    --clean-hashes '["28ee428f75efe2058e87c6ae39fbfee0f1bfc9fa5a51464826cf868ceb982285"]' \
    --reward-file /logs/verifier/reward.txt

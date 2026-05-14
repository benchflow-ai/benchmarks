#!/bin/bash
# Verifier for ProgramBench task: tomnomnom__gron.88a6234
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "tomnomnom__gron.88a6234" \
    --workspace /workspace \
    --clean-hashes '[]' \
    --reward-file /logs/verifier/reward.txt

#!/bin/bash
# Verifier for ProgramBench task: mibk__dupl.1bf052b
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "mibk__dupl.1bf052b" \
    --workspace /workspace \
    --clean-hashes '["eefa7175d91c59c1e305e3d4e84ca46fbb3a65b715d2a4436ebfa3ba2f1fe9f4"]' \
    --reward-file /logs/verifier/reward.txt

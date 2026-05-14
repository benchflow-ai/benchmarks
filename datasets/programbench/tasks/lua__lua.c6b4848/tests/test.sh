#!/bin/bash
# Verifier for ProgramBench task: lua__lua.c6b4848
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "lua__lua.c6b4848" \
    --workspace /workspace \
    --clean-hashes '["46d302c1de7129b3d29763c94dee7c8aff2ce91ce679043fb847c249475ad5c8"]' \
    --reward-file /logs/verifier/reward.txt

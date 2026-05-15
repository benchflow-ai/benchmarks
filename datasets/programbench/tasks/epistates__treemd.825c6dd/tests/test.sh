#!/bin/bash
# Verifier for ProgramBench task: epistates__treemd.825c6dd
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "epistates__treemd.825c6dd" \
    --workspace /workspace \
    --clean-hashes '["789a522be781ab22e230304cece5ce356e7369b876f7b57682639c6a6a7d42b1"]' \
    --reward-file /logs/verifier/reward.txt

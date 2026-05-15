#!/bin/bash
# Verifier for ProgramBench task: mkj__dropbear.75f699b
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "mkj__dropbear.75f699b" \
    --workspace /workspace \
    --clean-hashes '["516684046597d6b1178ae0e85aee2f025b8efc185abadc3219c6198a772716a9"]' \
    --reward-file /logs/verifier/reward.txt

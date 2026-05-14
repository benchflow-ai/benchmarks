#!/bin/bash
# Verifier for ProgramBench task: orf__gping.26eb5b9
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "orf__gping.26eb5b9" \
    --workspace /workspace \
    --clean-hashes '["53fdb9ecac67dacba76d1bcdf8bf7f71d7d0e91ac7c4f73721904049fb650291"]' \
    --reward-file /logs/verifier/reward.txt

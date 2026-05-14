#!/bin/bash
# Verifier for ProgramBench task: trasta298__keifu.3331426
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "trasta298__keifu.3331426" \
    --workspace /workspace \
    --clean-hashes '["5a9fa8020383b39abc7f530372f409f01b4d0ec3f89926d68492728e2ee26c55"]' \
    --reward-file /logs/verifier/reward.txt

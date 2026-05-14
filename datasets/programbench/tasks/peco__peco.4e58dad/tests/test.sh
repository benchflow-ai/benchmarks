#!/bin/bash
# Verifier for ProgramBench task: peco__peco.4e58dad
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "peco__peco.4e58dad" \
    --workspace /workspace \
    --clean-hashes '["ef799b52e5e820c8f91eeeb98fd9a069058101f21ae8ee04cc5763d972a229d8"]' \
    --reward-file /logs/verifier/reward.txt

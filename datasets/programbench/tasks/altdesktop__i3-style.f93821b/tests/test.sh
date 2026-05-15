#!/bin/bash
# Verifier for ProgramBench task: altdesktop__i3-style.f93821b
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "altdesktop__i3-style.f93821b" \
    --workspace /workspace \
    --clean-hashes '["05a7ef5341ac0a1d437f0b4d547badf376f951cc51578f01a91a279519a8215b"]' \
    --reward-file /logs/verifier/reward.txt

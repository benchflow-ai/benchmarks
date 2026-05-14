#!/bin/bash
# Verifier for ProgramBench task: ammarabouzor__tui-journal.2b4540d
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "ammarabouzor__tui-journal.2b4540d" \
    --workspace /workspace \
    --clean-hashes '["54ce16f94b2370b44274b080b5ef1f6f7116f71b00e1f8d7084c9e921dca9eb9"]' \
    --reward-file /logs/verifier/reward.txt

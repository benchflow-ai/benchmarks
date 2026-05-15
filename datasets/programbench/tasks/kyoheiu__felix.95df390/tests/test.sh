#!/bin/bash
# Verifier for ProgramBench task: kyoheiu__felix.95df390
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "kyoheiu__felix.95df390" \
    --workspace /workspace \
    --clean-hashes '["4c2d80b1e22f8279346a8591f448547e7aab315983eb7678b651d1e3110068d1"]' \
    --reward-file /logs/verifier/reward.txt

#!/bin/bash
# Verifier for ProgramBench task: cslarsen__jp2a.61d205f
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "cslarsen__jp2a.61d205f" \
    --workspace /workspace \
    --clean-hashes '["9ce1474cc1880d4cda602b823909c5edfd99ffcaa9eb4bca98115d89494a9e6f"]' \
    --reward-file /logs/verifier/reward.txt

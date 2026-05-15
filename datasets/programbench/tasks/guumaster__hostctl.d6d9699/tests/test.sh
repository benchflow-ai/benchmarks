#!/bin/bash
# Verifier for ProgramBench task: guumaster__hostctl.d6d9699
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "guumaster__hostctl.d6d9699" \
    --workspace /workspace \
    --clean-hashes '["2d3c78fb64b6291fab22a5bc5f31d4d4142fa12dc7ed843b2ae8decbb1413d70"]' \
    --reward-file /logs/verifier/reward.txt

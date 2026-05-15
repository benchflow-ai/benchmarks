#!/bin/bash
# Verifier for ProgramBench task: typst__typst.88356d0
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "typst__typst.88356d0" \
    --workspace /workspace \
    --clean-hashes '["8252dc8ed19ecfdcf92081c7324447b705ad30ae62c7d57c393e60966e518a55"]' \
    --reward-file /logs/verifier/reward.txt

#!/bin/bash
# Verifier for ProgramBench task: byron__dua-cli.8570c15
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "byron__dua-cli.8570c15" \
    --workspace /workspace \
    --clean-hashes '["50ddfcf2b47205cbf31aa1c8230a266d33ef522371a9e58a5bc1fad56d0a2e4e"]' \
    --reward-file /logs/verifier/reward.txt

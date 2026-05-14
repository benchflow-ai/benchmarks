#!/bin/bash
# Verifier for ProgramBench task: oppiliappan__statix.e9df54c
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "oppiliappan__statix.e9df54c" \
    --workspace /workspace \
    --clean-hashes '["446df25ba1c96de6591972df8aa82aeff7c9f701a60d532afcec37964a15d5e0"]' \
    --reward-file /logs/verifier/reward.txt

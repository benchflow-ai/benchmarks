#!/bin/bash
# Verifier for ProgramBench task: dandavison__delta.acd758f
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "dandavison__delta.acd758f" \
    --workspace /workspace \
    --clean-hashes '["2140df34c5cb9397afd019e7ad100535c0c15182845e65095d13cc4bb6987a3f"]' \
    --reward-file /logs/verifier/reward.txt

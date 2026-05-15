#!/bin/bash
# Verifier for ProgramBench task: drew-alleman__datasurgeon.d257cee
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "drew-alleman__datasurgeon.d257cee" \
    --workspace /workspace \
    --clean-hashes '["0fad3f3c8c55c98de87355da7bf454a8a5f83ed4c9ce012a389fee75f92d0511"]' \
    --reward-file /logs/verifier/reward.txt

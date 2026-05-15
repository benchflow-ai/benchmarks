#!/bin/bash
# Verifier for ProgramBench task: naggie__dstask.ff57396
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "naggie__dstask.ff57396" \
    --workspace /workspace \
    --clean-hashes '["c4620cf024a7d6f9842a4edece55e8680985bff3829dc8895e8f76d70b85423f"]' \
    --reward-file /logs/verifier/reward.txt

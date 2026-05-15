#!/bin/bash
# Verifier for ProgramBench task: sstadick__hck.b66c751
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "sstadick__hck.b66c751" \
    --workspace /workspace \
    --clean-hashes '["de16846838a2842a14f68ec9368237d4c5402eb9875bf4f535d9b2d1ffed71b4"]' \
    --reward-file /logs/verifier/reward.txt

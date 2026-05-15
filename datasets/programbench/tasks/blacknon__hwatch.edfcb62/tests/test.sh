#!/bin/bash
# Verifier for ProgramBench task: blacknon__hwatch.edfcb62
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "blacknon__hwatch.edfcb62" \
    --workspace /workspace \
    --clean-hashes '["04e9012ef5ff966b95f7e8d33f6d3ef7a0c70e444514fc05570c67207971f755"]' \
    --reward-file /logs/verifier/reward.txt

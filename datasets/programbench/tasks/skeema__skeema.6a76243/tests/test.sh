#!/bin/bash
# Verifier for ProgramBench task: skeema__skeema.6a76243
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "skeema__skeema.6a76243" \
    --workspace /workspace \
    --clean-hashes '["074226d3e39a852ad1eddc97817495cf01f21309e8ba710f22de8af8f8b9ab3f"]' \
    --reward-file /logs/verifier/reward.txt

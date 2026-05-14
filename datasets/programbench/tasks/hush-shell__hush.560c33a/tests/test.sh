#!/bin/bash
# Verifier for ProgramBench task: hush-shell__hush.560c33a
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "hush-shell__hush.560c33a" \
    --workspace /workspace \
    --clean-hashes '["f036d5a688fcbc210730071f3b5791fdfc64af3723931eda07c2a9c050aca7c9"]' \
    --reward-file /logs/verifier/reward.txt

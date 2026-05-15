#!/bin/bash
# Verifier for ProgramBench task: tukaani-project__xz.1007bf0
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "tukaani-project__xz.1007bf0" \
    --workspace /workspace \
    --clean-hashes '["40acc91528155a61364fb295efc7d4dadb042d3e187cec95096a6d62d2585f26"]' \
    --reward-file /logs/verifier/reward.txt

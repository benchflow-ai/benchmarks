#!/bin/bash
# Verifier for ProgramBench task: jqlang__jq.b33a763
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "jqlang__jq.b33a763" \
    --workspace /workspace \
    --clean-hashes '["6ca182a6c27d6e7081f23fc70d09a6030f05dab810504644c0bd3ff3869f12b6"]' \
    --reward-file /logs/verifier/reward.txt

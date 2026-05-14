#!/bin/bash
# Verifier for ProgramBench task: mgdm__htmlq.6e31bc8
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "mgdm__htmlq.6e31bc8" \
    --workspace /workspace \
    --clean-hashes '["b7985a789a31f8939072bd488f2e461e9e35724b2fbee2cf386ef474a41efd4c"]' \
    --reward-file /logs/verifier/reward.txt

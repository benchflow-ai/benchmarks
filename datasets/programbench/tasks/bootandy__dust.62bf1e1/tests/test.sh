#!/bin/bash
# Verifier for ProgramBench task: bootandy__dust.62bf1e1
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "bootandy__dust.62bf1e1" \
    --workspace /workspace \
    --clean-hashes '["49dc6200ab5e315f783f7ad3f7a7af4d758b49053bccc689b8ff33b3d0613f4c"]' \
    --reward-file /logs/verifier/reward.txt

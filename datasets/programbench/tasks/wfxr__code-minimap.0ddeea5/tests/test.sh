#!/bin/bash
# Verifier for ProgramBench task: wfxr__code-minimap.0ddeea5
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "wfxr__code-minimap.0ddeea5" \
    --workspace /workspace \
    --clean-hashes '["b1c0790a7394e68435755f487877512cb9740395010c804e70242f5e8d752bb6"]' \
    --reward-file /logs/verifier/reward.txt

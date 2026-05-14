#!/bin/bash
# Verifier for ProgramBench task: ys-l__flamelens.0b4dc33
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "ys-l__flamelens.0b4dc33" \
    --workspace /workspace \
    --clean-hashes '["07e80f0ed55ace5a8284d97894aabc0a5417366d85adb233365a2937a608a130"]' \
    --reward-file /logs/verifier/reward.txt

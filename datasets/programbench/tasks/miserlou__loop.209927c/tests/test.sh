#!/bin/bash
# Verifier for ProgramBench task: miserlou__loop.209927c
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "miserlou__loop.209927c" \
    --workspace /workspace \
    --clean-hashes '["c1f712b36db980f69daf4c18fa0516f2663dc9917aae836d0fdc24f45783b395"]' \
    --reward-file /logs/verifier/reward.txt

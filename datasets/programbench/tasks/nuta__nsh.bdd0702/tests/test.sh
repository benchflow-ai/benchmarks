#!/bin/bash
# Verifier for ProgramBench task: nuta__nsh.bdd0702
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "nuta__nsh.bdd0702" \
    --workspace /workspace \
    --clean-hashes '["ab3d07a2de6f7362ee34e0e9add770fa9a87188bad1c8cfdb6007b4ff6c91f05"]' \
    --reward-file /logs/verifier/reward.txt

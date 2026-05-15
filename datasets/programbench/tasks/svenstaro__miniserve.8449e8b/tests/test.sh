#!/bin/bash
# Verifier for ProgramBench task: svenstaro__miniserve.8449e8b
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "svenstaro__miniserve.8449e8b" \
    --workspace /workspace \
    --clean-hashes '["3c205d4e64b02fe2a42102572db8142e55788a0e10c01c0c987ff39d57dfcefc"]' \
    --reward-file /logs/verifier/reward.txt

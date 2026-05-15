#!/bin/bash
# Verifier for ProgramBench task: esubaalew__run.0fb9dec
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "esubaalew__run.0fb9dec" \
    --workspace /workspace \
    --clean-hashes '["4355a3374ea9851541d1a1e0370de158cceb8d973094b79463d9a4b822ab9fe8"]' \
    --reward-file /logs/verifier/reward.txt

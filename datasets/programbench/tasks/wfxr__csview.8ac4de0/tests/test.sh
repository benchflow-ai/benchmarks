#!/bin/bash
# Verifier for ProgramBench task: wfxr__csview.8ac4de0
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "wfxr__csview.8ac4de0" \
    --workspace /workspace \
    --clean-hashes '["e07420f640d1e6a0c047cab49431d1b561f661241efe111a053ff5dde1119d09"]' \
    --reward-file /logs/verifier/reward.txt

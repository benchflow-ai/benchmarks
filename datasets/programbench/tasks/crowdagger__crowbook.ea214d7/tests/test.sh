#!/bin/bash
# Verifier for ProgramBench task: crowdagger__crowbook.ea214d7
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "crowdagger__crowbook.ea214d7" \
    --workspace /workspace \
    --clean-hashes '["30fe43c188f080026577d2fa935ebf33f0b902077bb2138724f839680eb45944"]' \
    --reward-file /logs/verifier/reward.txt

#!/bin/bash
# Verifier for ProgramBench task: rs__curlie.5dfcbb1
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "rs__curlie.5dfcbb1" \
    --workspace /workspace \
    --clean-hashes '["e7e4f84ba194306ef782853d8b77788dd4674a6baad19c878885bb08c2db0d35"]' \
    --reward-file /logs/verifier/reward.txt

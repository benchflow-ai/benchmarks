#!/bin/bash
# Verifier for ProgramBench task: htop-dev__htop.523600b
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "htop-dev__htop.523600b" \
    --workspace /workspace \
    --clean-hashes '["3bccdc16b5be8d734ffe88dba5ac9e861c6a8923d7434d9cd250719766db4a5d"]' \
    --reward-file /logs/verifier/reward.txt

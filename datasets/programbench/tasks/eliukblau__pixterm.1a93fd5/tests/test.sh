#!/bin/bash
# Verifier for ProgramBench task: eliukblau__pixterm.1a93fd5
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "eliukblau__pixterm.1a93fd5" \
    --workspace /workspace \
    --clean-hashes '["ce3ca3b31f37c0334db3f836f4bd848ffe2d2a553e1c2bf3f465b7fc6f6511c0"]' \
    --reward-file /logs/verifier/reward.txt

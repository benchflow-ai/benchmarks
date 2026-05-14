#!/bin/bash
# Verifier for ProgramBench task: cweill__gotests.2a672c5
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "cweill__gotests.2a672c5" \
    --workspace /workspace \
    --clean-hashes '["78f5a9425a6867739c7f8aa7bc2a5d9058bae9a684149667da07e194b35aebdb"]' \
    --reward-file /logs/verifier/reward.txt

#!/bin/bash
# Verifier for ProgramBench task: rcoh__angle-grinder.9c2fc88
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "rcoh__angle-grinder.9c2fc88" \
    --workspace /workspace \
    --clean-hashes '[]' \
    --reward-file /logs/verifier/reward.txt

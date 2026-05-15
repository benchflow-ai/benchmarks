#!/bin/bash
# Verifier for ProgramBench task: ekzhang__bore.8e059cd
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "ekzhang__bore.8e059cd" \
    --workspace /workspace \
    --clean-hashes '["e7464f4078a4be427e752bfdd7aae891f74287fe0afe4c347a31d87b204467ff"]' \
    --reward-file /logs/verifier/reward.txt

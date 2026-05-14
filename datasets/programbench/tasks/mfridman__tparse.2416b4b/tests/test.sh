#!/bin/bash
# Verifier for ProgramBench task: mfridman__tparse.2416b4b
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "mfridman__tparse.2416b4b" \
    --workspace /workspace \
    --clean-hashes '["45d4c1e593b02ebef000be4d4918c32dc5f20b6b2b69f5c7f13ba7d222d1a24a"]' \
    --reward-file /logs/verifier/reward.txt

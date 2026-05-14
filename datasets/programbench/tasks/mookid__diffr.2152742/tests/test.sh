#!/bin/bash
# Verifier for ProgramBench task: mookid__diffr.2152742
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "mookid__diffr.2152742" \
    --workspace /workspace \
    --clean-hashes '["7e458441195a4027d8993abdec026f65d6e5929dabf2e3a5aeb18664c94c29b5"]' \
    --reward-file /logs/verifier/reward.txt

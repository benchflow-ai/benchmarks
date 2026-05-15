#!/bin/bash
# Verifier for ProgramBench task: ariga__atlas.6d81150
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "ariga__atlas.6d81150" \
    --workspace /workspace \
    --clean-hashes '["116cacacf782ebd501c782d9d546985bb0f347040e024e8ce7728fb222e2f06a"]' \
    --reward-file /logs/verifier/reward.txt

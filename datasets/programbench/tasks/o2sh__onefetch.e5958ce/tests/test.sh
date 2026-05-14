#!/bin/bash
# Verifier for ProgramBench task: o2sh__onefetch.e5958ce
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "o2sh__onefetch.e5958ce" \
    --workspace /workspace \
    --clean-hashes '["f7575b3db03cdfea674563ab0e5bea842e896f21145a96a8d4ec41293605f66a"]' \
    --reward-file /logs/verifier/reward.txt

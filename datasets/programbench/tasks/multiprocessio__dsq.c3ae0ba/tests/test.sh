#!/bin/bash
# Verifier for ProgramBench task: multiprocessio__dsq.c3ae0ba
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "multiprocessio__dsq.c3ae0ba" \
    --workspace /workspace \
    --clean-hashes '["77230db960a916339b1db750631531c1cb165883b5cd7b705a8fa4c2cce33522"]' \
    --reward-file /logs/verifier/reward.txt

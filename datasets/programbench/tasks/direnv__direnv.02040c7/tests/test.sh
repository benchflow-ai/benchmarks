#!/bin/bash
# Verifier for ProgramBench task: direnv__direnv.02040c7
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "direnv__direnv.02040c7" \
    --workspace /workspace \
    --clean-hashes '["192c8bccc1fb988a4bec94e336ff54a1057e8afe74ce78db31fb1b380c16d88d"]' \
    --reward-file /logs/verifier/reward.txt

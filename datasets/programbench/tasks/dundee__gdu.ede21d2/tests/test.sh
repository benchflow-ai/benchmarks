#!/bin/bash
# Verifier for ProgramBench task: dundee__gdu.ede21d2
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "dundee__gdu.ede21d2" \
    --workspace /workspace \
    --clean-hashes '["47c41ab7e8ff7e0b8dcf0e6134670c12ca1b5c38919567202a1471fee5211c40"]' \
    --reward-file /logs/verifier/reward.txt

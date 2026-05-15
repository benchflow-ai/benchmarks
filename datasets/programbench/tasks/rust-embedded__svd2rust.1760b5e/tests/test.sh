#!/bin/bash
# Verifier for ProgramBench task: rust-embedded__svd2rust.1760b5e
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "rust-embedded__svd2rust.1760b5e" \
    --workspace /workspace \
    --clean-hashes '["c8fb9356ae6571da2859431b401a5a7bf392537ae9e15178f7deeaecf0d4f1fc"]' \
    --reward-file /logs/verifier/reward.txt

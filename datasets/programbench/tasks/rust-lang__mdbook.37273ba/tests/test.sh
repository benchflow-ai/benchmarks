#!/bin/bash
# Verifier for ProgramBench task: rust-lang__mdbook.37273ba
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "rust-lang__mdbook.37273ba" \
    --workspace /workspace \
    --clean-hashes '["5a727dd478395718d5969cad16e9886fcb23391429ffa1c0ad239940356fbe4a"]' \
    --reward-file /logs/verifier/reward.txt

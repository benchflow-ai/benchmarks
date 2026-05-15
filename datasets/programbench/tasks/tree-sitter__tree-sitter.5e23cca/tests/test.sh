#!/bin/bash
# Verifier for ProgramBench task: tree-sitter__tree-sitter.5e23cca
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "tree-sitter__tree-sitter.5e23cca" \
    --workspace /workspace \
    --clean-hashes '["4a800e7f990b77c69d1cabcba1417cd4c256d70420091c81825a0201bcc96a77"]' \
    --reward-file /logs/verifier/reward.txt

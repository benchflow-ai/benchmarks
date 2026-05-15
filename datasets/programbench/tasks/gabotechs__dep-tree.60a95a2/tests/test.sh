#!/bin/bash
# Verifier for ProgramBench task: gabotechs__dep-tree.60a95a2
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "gabotechs__dep-tree.60a95a2" \
    --workspace /workspace \
    --clean-hashes '["8a127b03fb358c6bef561984731938a3ce60cc3354bb9b5aace6d3ef7b6c68a0"]' \
    --reward-file /logs/verifier/reward.txt

#!/bin/bash
# Verifier for ProgramBench task: git-bahn__git-graph.87b4473
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "git-bahn__git-graph.87b4473" \
    --workspace /workspace \
    --clean-hashes '["f406a9f2246192fed2f4e583a85ee2b07af1aea46edb61fb90dc9e74f5c4b17a"]' \
    --reward-file /logs/verifier/reward.txt

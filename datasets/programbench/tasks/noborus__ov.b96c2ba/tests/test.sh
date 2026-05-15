#!/bin/bash
# Verifier for ProgramBench task: noborus__ov.b96c2ba
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "noborus__ov.b96c2ba" \
    --workspace /workspace \
    --clean-hashes '["1ae60e06e5cc8e795b9f0b4d15117ad6d193b2eaf64b13da7dcfea46aef73378"]' \
    --reward-file /logs/verifier/reward.txt

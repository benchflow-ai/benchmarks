#!/bin/bash
# Verifier for ProgramBench task: antonmedv__fx.86d0d34
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "antonmedv__fx.86d0d34" \
    --workspace /workspace \
    --clean-hashes '["dc56432225fae7b9befca1e8e781ab52cd700eb9404a31d0cf351324025f2587"]' \
    --reward-file /logs/verifier/reward.txt

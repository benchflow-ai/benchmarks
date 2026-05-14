#!/bin/bash
# Verifier for ProgramBench task: segmentio__chamber.5f93f5f
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "segmentio__chamber.5f93f5f" \
    --workspace /workspace \
    --clean-hashes '["77f1d290b5d1d201483b042be115e89fb7d2b9b23bdd08708a511842be34c584"]' \
    --reward-file /logs/verifier/reward.txt

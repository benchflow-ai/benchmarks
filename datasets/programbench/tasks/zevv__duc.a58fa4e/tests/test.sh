#!/bin/bash
# Verifier for ProgramBench task: zevv__duc.a58fa4e
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "zevv__duc.a58fa4e" \
    --workspace /workspace \
    --clean-hashes '["b724715fee63228119ea9caeb3f4b436f618d8a8752138a73367063b768d20a2"]' \
    --reward-file /logs/verifier/reward.txt

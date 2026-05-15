#!/bin/bash
# Verifier for ProgramBench task: elkowar__pipr.fae0b17
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "elkowar__pipr.fae0b17" \
    --workspace /workspace \
    --clean-hashes '["e695f2632749184df9dd7e96be91e6932a4825295c6ea3694a620895439fc854"]' \
    --reward-file /logs/verifier/reward.txt

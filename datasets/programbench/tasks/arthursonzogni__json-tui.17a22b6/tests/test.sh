#!/bin/bash
# Verifier for ProgramBench task: arthursonzogni__json-tui.17a22b6
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "arthursonzogni__json-tui.17a22b6" \
    --workspace /workspace \
    --clean-hashes '["4349db9afad22577dac9848f201b520838a1ffd602ed68f02d24a2551e58aaff"]' \
    --reward-file /logs/verifier/reward.txt

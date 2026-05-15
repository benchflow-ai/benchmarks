#!/bin/bash
# Verifier for ProgramBench task: nikolassv__bartib.6b9b5ce
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "nikolassv__bartib.6b9b5ce" \
    --workspace /workspace \
    --clean-hashes '["a8658eff2fef4c4b3c502f0b48922a2acb198a4559d26f953f22b461877fc0d7"]' \
    --reward-file /logs/verifier/reward.txt

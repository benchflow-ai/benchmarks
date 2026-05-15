#!/bin/bash
# Verifier for ProgramBench task: pier-cli__pier.5e1bde9
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "pier-cli__pier.5e1bde9" \
    --workspace /workspace \
    --clean-hashes '["0abe2c8a0d566e7b93a7958a89ceb3ea3d3cd369e32cf8c2e7a0e1f703464988"]' \
    --reward-file /logs/verifier/reward.txt

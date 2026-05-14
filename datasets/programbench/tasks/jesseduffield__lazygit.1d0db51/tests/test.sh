#!/bin/bash
# Verifier for ProgramBench task: jesseduffield__lazygit.1d0db51
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "jesseduffield__lazygit.1d0db51" \
    --workspace /workspace \
    --clean-hashes '["8f671f19efc6626df5dda1b02448e9d4ac76b92b5b9cce45df61a126a65833f8"]' \
    --reward-file /logs/verifier/reward.txt

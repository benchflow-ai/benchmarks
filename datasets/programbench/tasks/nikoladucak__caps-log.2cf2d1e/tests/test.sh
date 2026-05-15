#!/bin/bash
# Verifier for ProgramBench task: nikoladucak__caps-log.2cf2d1e
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "nikoladucak__caps-log.2cf2d1e" \
    --workspace /workspace \
    --clean-hashes '["b51ce78846058777cafdf8fff9280acb7a3e0a5eff01dda36ad0464220374223"]' \
    --reward-file /logs/verifier/reward.txt

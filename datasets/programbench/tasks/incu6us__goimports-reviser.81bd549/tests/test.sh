#!/bin/bash
# Verifier for ProgramBench task: incu6us__goimports-reviser.81bd549
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "incu6us__goimports-reviser.81bd549" \
    --workspace /workspace \
    --clean-hashes '["d9a660ef333c4df431b8d329a755cc886566484c1705c6cbe0d249ec9f685bb9"]' \
    --reward-file /logs/verifier/reward.txt

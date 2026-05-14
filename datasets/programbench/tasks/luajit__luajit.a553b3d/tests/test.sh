#!/bin/bash
# Verifier for ProgramBench task: luajit__luajit.a553b3d
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "luajit__luajit.a553b3d" \
    --workspace /workspace \
    --clean-hashes '["a46fdc84f8d97b05fac8b4ac241bce8216a686ed52267f12f620c14bb50e88fc"]' \
    --reward-file /logs/verifier/reward.txt

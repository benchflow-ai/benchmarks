#!/bin/bash
# Verifier for ProgramBench task: burntsushi__xsv.f430466
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "burntsushi__xsv.f430466" \
    --workspace /workspace \
    --clean-hashes '["dd7cf0aa19bf5aeb10996e93f02a654e92a36309096f9102f40bc226843a816a"]' \
    --reward-file /logs/verifier/reward.txt

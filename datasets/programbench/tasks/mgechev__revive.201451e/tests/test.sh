#!/bin/bash
# Verifier for ProgramBench task: mgechev__revive.201451e
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "mgechev__revive.201451e" \
    --workspace /workspace \
    --clean-hashes '["7307244b0aac6830bab64879f6d2cdb764f4dc78c50b7df78683890474e30771"]' \
    --reward-file /logs/verifier/reward.txt

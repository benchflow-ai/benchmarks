#!/bin/bash
# Verifier for ProgramBench task: kisielk__errcheck.dacab89
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "kisielk__errcheck.dacab89" \
    --workspace /workspace \
    --clean-hashes '["296c10882ce659f773095e0d57cb517fcc0f8737044a24e6557231dd1f9da39b"]' \
    --reward-file /logs/verifier/reward.txt

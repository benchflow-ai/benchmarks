#!/bin/bash
# Verifier for ProgramBench task: sirwart__ripsecrets.34c9e03
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "sirwart__ripsecrets.34c9e03" \
    --workspace /workspace \
    --clean-hashes '["f070794787cc67b927a2538fe2a38761ae48115e72796ff5db703fb6206e60c4"]' \
    --reward-file /logs/verifier/reward.txt

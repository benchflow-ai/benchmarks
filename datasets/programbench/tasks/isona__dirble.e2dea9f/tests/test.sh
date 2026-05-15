#!/bin/bash
# Verifier for ProgramBench task: isona__dirble.e2dea9f
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "isona__dirble.e2dea9f" \
    --workspace /workspace \
    --clean-hashes '["f91362847bed99efb1b2423f79762c8a0b371d81a754e4dbb8f824f5164d4320"]' \
    --reward-file /logs/verifier/reward.txt

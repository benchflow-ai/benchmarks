#!/bin/bash
# Verifier for ProgramBench task: brocode__fblog.3b54330
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "brocode__fblog.3b54330" \
    --workspace /workspace \
    --clean-hashes '["aadfc28bdd1eb63dfc08b8ede5bd8ad73aa60ca1b664dfd28f13bdade7146a54"]' \
    --reward-file /logs/verifier/reward.txt

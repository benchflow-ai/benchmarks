#!/bin/bash
# Verifier for ProgramBench task: konradsz__igrep.aa75630
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "konradsz__igrep.aa75630" \
    --workspace /workspace \
    --clean-hashes '["b711b07750c89fe216d978499c0ab82cf67f5066b315a88915eae5366c81b38b"]' \
    --reward-file /logs/verifier/reward.txt

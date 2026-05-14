#!/bin/bash
# Verifier for ProgramBench task: samtools__samtools.aa823b5
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "samtools__samtools.aa823b5" \
    --workspace /workspace \
    --clean-hashes '[]' \
    --reward-file /logs/verifier/reward.txt

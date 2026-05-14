#!/bin/bash
# Verifier for ProgramBench task: unhappychoice__gittype.34b72d0
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "unhappychoice__gittype.34b72d0" \
    --workspace /workspace \
    --clean-hashes '["6c3345ab9a3b7f36c8a7427830191014df720a5d4b2b431934982d403f925a6b"]' \
    --reward-file /logs/verifier/reward.txt

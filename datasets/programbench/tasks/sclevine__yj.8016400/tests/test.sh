#!/bin/bash
# Verifier for ProgramBench task: sclevine__yj.8016400
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "sclevine__yj.8016400" \
    --workspace /workspace \
    --clean-hashes '["58174833025a6ceb4c124ceb281fc23da0da45b62356b4f87e7136ee3a14451c"]' \
    --reward-file /logs/verifier/reward.txt

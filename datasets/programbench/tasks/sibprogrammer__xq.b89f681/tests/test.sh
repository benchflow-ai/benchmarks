#!/bin/bash
# Verifier for ProgramBench task: sibprogrammer__xq.b89f681
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "sibprogrammer__xq.b89f681" \
    --workspace /workspace \
    --clean-hashes '["232f15fa8b6fc4594b301e3fc14ab3e78065bf23aa7b0785cbd44a306051b950"]' \
    --reward-file /logs/verifier/reward.txt

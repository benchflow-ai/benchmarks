#!/bin/bash
# Verifier for ProgramBench task: sharkdp__hexyl.2e26437
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "sharkdp__hexyl.2e26437" \
    --workspace /workspace \
    --clean-hashes '["a6fc6dcc471bfaf4ff37a24a810023dfeefa9c0652a07e4efdcdad2b404b776e"]' \
    --reward-file /logs/verifier/reward.txt

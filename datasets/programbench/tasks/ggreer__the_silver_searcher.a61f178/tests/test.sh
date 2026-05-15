#!/bin/bash
# Verifier for ProgramBench task: ggreer__the_silver_searcher.a61f178
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "ggreer__the_silver_searcher.a61f178" \
    --workspace /workspace \
    --clean-hashes '["07ae1b9a4e4943556996b3917b0bba5a43dedea19c738c274d9beb58cb4ed561"]' \
    --reward-file /logs/verifier/reward.txt

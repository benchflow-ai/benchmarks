#!/bin/bash
# Verifier for ProgramBench task: clog-tool__clog-cli.7066cba
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "clog-tool__clog-cli.7066cba" \
    --workspace /workspace \
    --clean-hashes '["8992cdf99f9dc6e1922ae72979042c7dda5b76f37e8c099301c8f8a6f76452e3"]' \
    --reward-file /logs/verifier/reward.txt

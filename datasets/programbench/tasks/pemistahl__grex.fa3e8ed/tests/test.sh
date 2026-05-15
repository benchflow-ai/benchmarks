#!/bin/bash
# Verifier for ProgramBench task: pemistahl__grex.fa3e8ed
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "pemistahl__grex.fa3e8ed" \
    --workspace /workspace \
    --clean-hashes '["ad96801fa83cdf1d1bf8565d75d3c455de6c74de9feef81b1841805ed47b30d3"]' \
    --reward-file /logs/verifier/reward.txt

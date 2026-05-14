#!/bin/bash
# Verifier for ProgramBench task: ksxgithub__parallel-disk-usage.96978ed
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "ksxgithub__parallel-disk-usage.96978ed" \
    --workspace /workspace \
    --clean-hashes '["fdc96130c94781485de07488273cadd5351977d8518e1f1390677633b6cd1c86"]' \
    --reward-file /logs/verifier/reward.txt

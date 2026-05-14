#!/bin/bash
# Verifier for ProgramBench task: lz4__lz4.1519f46
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "lz4__lz4.1519f46" \
    --workspace /workspace \
    --clean-hashes '["39482b2512114fc5e593949649b644a0eb9f10856baf8e579deb4e7a6161cefc"]' \
    --reward-file /logs/verifier/reward.txt

#!/bin/bash
# Verifier for ProgramBench task: parcel-bundler__lightningcss.aa2ed1e
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "parcel-bundler__lightningcss.aa2ed1e" \
    --workspace /workspace \
    --clean-hashes '["123ed57e7a10218733e76a44a20462286e9c35a3be8bc1fed2bdc6e515bb9c13"]' \
    --reward-file /logs/verifier/reward.txt

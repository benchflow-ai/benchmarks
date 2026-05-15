#!/bin/bash
# Verifier for ProgramBench task: jrnxf__thokr.09375ef
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "jrnxf__thokr.09375ef" \
    --workspace /workspace \
    --clean-hashes '["34aa5eaa60ccff8715a977701da8b5cfa7d8f257844a5437830dd217d422625a"]' \
    --reward-file /logs/verifier/reward.txt

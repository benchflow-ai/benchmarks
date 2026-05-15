#!/bin/bash
# Verifier for ProgramBench task: agourlay__zip-password-finder.704700d
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "agourlay__zip-password-finder.704700d" \
    --workspace /workspace \
    --clean-hashes '["49b9879a61cc55c6755476159101cb1bb49abb9a4e5cc9ba1988d7c64b610007"]' \
    --reward-file /logs/verifier/reward.txt

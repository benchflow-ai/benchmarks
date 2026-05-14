#!/bin/bash
# Verifier for ProgramBench task: lfos__calcurse.49180d5
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "lfos__calcurse.49180d5" \
    --workspace /workspace \
    --clean-hashes '["bffc523c9f38258c077a8959f179269710378cd45cea55c77c8a46a889db6912"]' \
    --reward-file /logs/verifier/reward.txt

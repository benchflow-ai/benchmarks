#!/bin/bash
# Verifier for ProgramBench task: lh3__seqtk.94e7070
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "lh3__seqtk.94e7070" \
    --workspace /workspace \
    --clean-hashes '["348c6e08241681487a4031afd1c34c6970409209adaed9e8a04330be0c0b1e7b"]' \
    --reward-file /logs/verifier/reward.txt

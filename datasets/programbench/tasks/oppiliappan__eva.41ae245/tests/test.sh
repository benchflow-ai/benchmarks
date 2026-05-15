#!/bin/bash
# Verifier for ProgramBench task: oppiliappan__eva.41ae245
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "oppiliappan__eva.41ae245" \
    --workspace /workspace \
    --clean-hashes '["24db5a04697d6be1afc7edde56b1b9116a70bb0fe81140a702e11ee53be39f1f"]' \
    --reward-file /logs/verifier/reward.txt

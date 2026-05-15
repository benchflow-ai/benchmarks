#!/bin/bash
# Verifier for ProgramBench task: astro__deadnix.d590041
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "astro__deadnix.d590041" \
    --workspace /workspace \
    --clean-hashes '["6830274e43aee25ec209852f2cde31cff5246a3423d9f92e92f437970b2ab593"]' \
    --reward-file /logs/verifier/reward.txt

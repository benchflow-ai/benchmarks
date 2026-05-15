#!/bin/bash
# Verifier for ProgramBench task: sharkdp__pastel.b60e899
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "sharkdp__pastel.b60e899" \
    --workspace /workspace \
    --clean-hashes '["858706582e9d30e509bca337e47257daac1c44cd1e0e1d4a422097d09bcca183"]' \
    --reward-file /logs/verifier/reward.txt

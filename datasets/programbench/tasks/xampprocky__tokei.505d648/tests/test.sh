#!/bin/bash
# Verifier for ProgramBench task: xampprocky__tokei.505d648
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "xampprocky__tokei.505d648" \
    --workspace /workspace \
    --clean-hashes '["aee46c9ad7c33acc835c295caae8b81f840e195104489d94fba7ce808592fc6f"]' \
    --reward-file /logs/verifier/reward.txt

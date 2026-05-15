#!/bin/bash
# Verifier for ProgramBench task: astaxie__bat.17d1080
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "astaxie__bat.17d1080" \
    --workspace /workspace \
    --clean-hashes '["786f4dc11f5ae09d90b2ff4a3ac96cabeab0954b196e7ebfe752afcc53245185"]' \
    --reward-file /logs/verifier/reward.txt

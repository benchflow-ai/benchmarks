#!/bin/bash
# Verifier for ProgramBench task: yaa110__nomino.f892499
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "yaa110__nomino.f892499" \
    --workspace /workspace \
    --clean-hashes '["824a5a0a983facff7bb8684cd278473875654c70dd32c022ae0e901a46ed0d4d"]' \
    --reward-file /logs/verifier/reward.txt

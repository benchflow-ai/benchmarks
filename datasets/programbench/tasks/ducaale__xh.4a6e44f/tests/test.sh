#!/bin/bash
# Verifier for ProgramBench task: ducaale__xh.4a6e44f
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "ducaale__xh.4a6e44f" \
    --workspace /workspace \
    --clean-hashes '["9598c4cdd80ac595e5480764a1bff4f2a609a93c22427c08bb02f122b72538a3"]' \
    --reward-file /logs/verifier/reward.txt

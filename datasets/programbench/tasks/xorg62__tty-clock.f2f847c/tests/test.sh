#!/bin/bash
# Verifier for ProgramBench task: xorg62__tty-clock.f2f847c
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "xorg62__tty-clock.f2f847c" \
    --workspace /workspace \
    --clean-hashes '["cd400708bcd6a5b9dd28bd450a211ec4625cde31470057e9d62f66072e297db0"]' \
    --reward-file /logs/verifier/reward.txt

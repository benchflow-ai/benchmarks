#!/bin/bash
# Verifier for ProgramBench task: cmatsuoka__figlet.202a0a8
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "cmatsuoka__figlet.202a0a8" \
    --workspace /workspace \
    --clean-hashes '["dd451146b1c0fcc67edf6569cfdc7ab237cc225fec41e6114eb0d759c701204d"]' \
    --reward-file /logs/verifier/reward.txt

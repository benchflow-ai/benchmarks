#!/bin/bash
# Verifier for ProgramBench task: axodotdev__oranda.27d60c7
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "axodotdev__oranda.27d60c7" \
    --workspace /workspace \
    --clean-hashes '["eeb2b26ba13333d2bd99f101649e3a25dbbfc986e553f3beef22da4277b59fe9"]' \
    --reward-file /logs/verifier/reward.txt

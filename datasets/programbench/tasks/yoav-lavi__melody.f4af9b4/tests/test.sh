#!/bin/bash
# Verifier for ProgramBench task: yoav-lavi__melody.f4af9b4
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "yoav-lavi__melody.f4af9b4" \
    --workspace /workspace \
    --clean-hashes '["0417aa95aa4732a732079df8c08ff0dfd8038867dc4894ea21488c49d7cfce03"]' \
    --reward-file /logs/verifier/reward.txt

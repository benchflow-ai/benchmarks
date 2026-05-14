#!/bin/bash
# Verifier for ProgramBench task: rs__jplot.2a54bcc
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "rs__jplot.2a54bcc" \
    --workspace /workspace \
    --clean-hashes '["ca593bbd96c07526d5d59ea58d4953f302b3f6b061f4042c5c05458dbaed33ba"]' \
    --reward-file /logs/verifier/reward.txt

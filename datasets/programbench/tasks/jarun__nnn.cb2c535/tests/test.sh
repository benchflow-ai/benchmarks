#!/bin/bash
# Verifier for ProgramBench task: jarun__nnn.cb2c535
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "jarun__nnn.cb2c535" \
    --workspace /workspace \
    --clean-hashes '["e014696296d4d415a13ed2cbd6939e6a0cb142964857da22b08a3ee67bacd9a6"]' \
    --reward-file /logs/verifier/reward.txt

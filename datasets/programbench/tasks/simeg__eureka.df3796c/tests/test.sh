#!/bin/bash
# Verifier for ProgramBench task: simeg__eureka.df3796c
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "simeg__eureka.df3796c" \
    --workspace /workspace \
    --clean-hashes '["1528514451c30447e93bc97bcda65118325cf80ceb92687716135f3ce12937aa"]' \
    --reward-file /logs/verifier/reward.txt

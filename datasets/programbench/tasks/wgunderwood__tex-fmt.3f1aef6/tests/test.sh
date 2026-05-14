#!/bin/bash
# Verifier for ProgramBench task: wgunderwood__tex-fmt.3f1aef6
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "wgunderwood__tex-fmt.3f1aef6" \
    --workspace /workspace \
    --clean-hashes '["7ada12e17ade344f5691b22d112623750cfcffc1185594e974ff11623978a138"]' \
    --reward-file /logs/verifier/reward.txt

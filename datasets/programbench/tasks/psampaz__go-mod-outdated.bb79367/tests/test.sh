#!/bin/bash
# Verifier for ProgramBench task: psampaz__go-mod-outdated.bb79367
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "psampaz__go-mod-outdated.bb79367" \
    --workspace /workspace \
    --clean-hashes '["3654bb785bf8cb76a99eb5233b5c8051699497df924df1c75ac8adbcbe6de929"]' \
    --reward-file /logs/verifier/reward.txt

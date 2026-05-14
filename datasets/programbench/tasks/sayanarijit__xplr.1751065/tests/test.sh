#!/bin/bash
# Verifier for ProgramBench task: sayanarijit__xplr.1751065
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "sayanarijit__xplr.1751065" \
    --workspace /workspace \
    --clean-hashes '["7faad8569632b1d8a4a049178debfa37eb2476b1be96bd588f66f25a7dbd4acb"]' \
    --reward-file /logs/verifier/reward.txt

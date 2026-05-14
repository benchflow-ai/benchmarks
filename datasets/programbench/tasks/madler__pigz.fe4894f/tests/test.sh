#!/bin/bash
# Verifier for ProgramBench task: madler__pigz.fe4894f
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "madler__pigz.fe4894f" \
    --workspace /workspace \
    --clean-hashes '["59fdb11c46c826db6b45778a38dcc2669a78ed9cc1932c4543f7ca43a322fda7"]' \
    --reward-file /logs/verifier/reward.txt

#!/bin/bash
# Verifier for ProgramBench task: kaushiksrini__parqeye.8072121
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "kaushiksrini__parqeye.8072121" \
    --workspace /workspace \
    --clean-hashes '["78d90daae4c1f1b549df73973f1ca41b6ff6cd351da2c17461246128de847661"]' \
    --reward-file /logs/verifier/reward.txt

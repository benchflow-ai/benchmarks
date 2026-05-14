#!/bin/bash
# Verifier for ProgramBench task: johanneskaufmann__html-to-markdown.3006818
# Compiles the agent's submission, downloads test blobs, runs behavioral tests.
set -o pipefail

exec > >(tee /logs/verifier/verifier.log) 2>&1

python3 /tests/verify.py \
    --instance-id "johanneskaufmann__html-to-markdown.3006818" \
    --workspace /workspace \
    --clean-hashes '["2255b718c18c5e12f490a6bb66eb920122a3988f60cbd657b0468792cdf427ae"]' \
    --reward-file /logs/verifier/reward.txt

#!/bin/bash
set -e

# Run the LLM-as-judge evaluator
python3 /tests/evaluate.py \
    --rubric /app/rubric.json \
    --output-dir /app \
    --reward-file /logs/verifier/reward.txt

exit 0

# BenchFlow Benchmarks

Standardized benchmark definitions for [BenchFlow](https://github.com/benchflow-ai/benchflow) — multi-turn agent benchmarking with ACP.

## Structure

Each benchmark lives in its own directory with a standard set of files:

```
benchmarks/
├── harvey-lab/
│   ├── benchmark.yaml        # standard benchmark descriptor
│   ├── benchflow.py          # converter: source format → BenchFlow tasks
│   ├── parity_test.py        # parity validation tests
│   ├── parity_experiment.json # parity results
│   └── README.md
├── <next-benchmark>/
│   ├── benchmark.yaml
│   └── ...
```

### benchmark.yaml

Every benchmark ships a `benchmark.yaml` — the standard descriptor declaring what the benchmark is, how tasks are verified, and parity validation results:

```yaml
name: my-benchmark
description: "Short description"
url: https://github.com/org/original-benchmark
author: BenchFlow

tasks:
  count: 100
  categories: 5
  tags: [coding, debugging]

conversion:
  script: benchflow.py
  source_format: task.json
  has_oracle_solutions: true

verification:
  method: unit-test            # or llm-as-judge
  reward: binary               # or proportional

parity:
  structural: { tasks_tested: 100, passed: 100 }
  side_by_side: { criteria_compared: 50, agreed: 48, agreement_rate: 0.96 }
```

### Converted Tasks on HuggingFace

Pre-converted BenchFlow task directories are published to [benchflow/benchmarks](https://huggingface.co/datasets/benchflow/benchmarks) on HuggingFace, so users can pull ready-to-run tasks without running the converter locally.

## Available Benchmarks

| Benchmark | Tasks | Verification | Parity |
|---|---|---|---|
| [harvey-lab](harvey-lab/) | 1,251 legal tasks, 24 practice areas | LLM-as-judge (Gemini) | 25/25 (100%) |

## Adding a New Benchmark

1. Create `benchmarks/<name>/` with `benchmark.yaml` and `benchflow.py`
2. Run parity tests and record results in `parity_experiment.json`
3. Upload converted tasks to HuggingFace
4. Submit a PR

See the [Harvey LAB benchmark](harvey-lab/) as a reference implementation.

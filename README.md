# BenchFlow Benchmarks

Ready-to-run benchmark task directories and parity experiments for [BenchFlow](https://github.com/benchflow-ai/benchflow).

This repo contains **converted tasks** and **parity results** — the output of running each benchmark's converter and validation pipeline. Conversion code, parity tests, and `benchmark.yaml` descriptors live in the main [benchflow](https://github.com/benchflow-ai/benchflow) repo under `benchmarks/<name>/`.

## Structure

```
datasets/
├── harvey-lab/
│   ├── benchmark.yaml            # standard benchmark descriptor
│   ├── README.md
│   ├── parity/
│   │   └── parity_experiment.json # side-by-side parity results
│   └── tasks/
│       ├── <task-id>/
│       │   ├── task.toml
│       │   ├── instruction.md
│       │   ├── environment/
│       │   │   └── Dockerfile
│       │   └── tests/
│       │       ├── test.sh
│       │       └── evaluate.py
│       └── ...
└── <next-benchmark>/
    └── ...
```

Each task directory follows the BenchFlow task format:
- `task.toml` — task metadata and configuration
- `instruction.md` — agent instructions
- `environment/Dockerfile` — container setup
- `tests/test.sh` — verifier entry point
- `tests/evaluate.py` — evaluation logic (for LLM-as-judge benchmarks)
- `solution/solve.sh` — oracle solution (when available)

## Available Datasets

| Dataset | Tasks | Verification | Parity | Source |
|---|---|---|---|---|
| [harvey-lab](datasets/harvey-lab/) | 1,251 | LLM-as-judge | 25/25 (100%) | [Harvey LAB](https://github.com/harveyai/harvey-labs) |

## Also on HuggingFace

Pre-converted tasks and parity results are also published to [benchflow/benchmarks](https://huggingface.co/datasets/benchflow/benchmarks) on HuggingFace.

## Usage

```bash
# Clone and run with BenchFlow
git clone https://github.com/benchflow-ai/benchmarks.git
cd benchmarks
benchflow run -t datasets/harvey-lab/tasks/<task-id>

# Or use from the benchflow repo with auto-download
python benchmarks/harvey-lab/run_harvey_lab.py
```

## Adding a Dataset

1. Write a converter in `benchflow-ai/benchflow/benchmarks/<name>/`
2. Run parity tests and record results
3. Generate all tasks and add them under `datasets/<name>/tasks/`
4. Add parity results under `datasets/<name>/parity/`
5. Submit a PR

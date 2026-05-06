# BenchFlow Benchmarks

Ready-to-run benchmark task directories for [BenchFlow](https://github.com/benchflow-ai/benchflow).

This repo contains the **converted tasks** — the output of running each benchmark's converter. Conversion code, parity tests, and `benchmark.yaml` descriptors live in the main [benchflow](https://github.com/benchflow-ai/benchflow) repo under `benchmarks/<name>/`.

## Structure

```
datasets/
├── harvey-lab/
│   ├── <task-id>/
│   │   ├── task.toml
│   │   ├── instruction.md
│   │   ├── environment/
│   │   │   └── Dockerfile
│   │   └── tests/
│   │       ├── test.sh
│   │       └── evaluate.py
│   └── ...
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

| Dataset | Tasks | Source |
|---|---|---|
| [harvey-lab](datasets/harvey-lab/) | 1,251 legal tasks | [Harvey LAB](https://github.com/harveyai/harvey-labs) |

## Also on HuggingFace

Pre-converted tasks are also published to [benchflow/benchmarks](https://huggingface.co/datasets/benchflow/benchmarks) on HuggingFace.

## Usage

```bash
# Clone and run with BenchFlow
git clone https://github.com/benchflow-ai/benchmarks.git
cd benchmarks
benchflow run -t datasets/harvey-lab/<task-id>

# Or use from the benchflow repo with auto-download
python benchmarks/harvey-lab/run_harvey_lab.py
```

## Adding a Dataset

1. Write a converter in `benchflow-ai/benchflow/benchmarks/<name>/`
2. Run parity tests
3. Generate all tasks and add them under `datasets/<name>/`
4. Submit a PR

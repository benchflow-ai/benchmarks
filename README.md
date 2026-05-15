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
├── programbench/
│   ├── parity/
│   │   └── parity_experiment.json  # agent + pipeline parity results
│   └── tasks/
│       ├── <owner>__<repo>.<commit>/
│       │   ├── task.toml
│       │   ├── instruction.md
│       │   ├── environment/
│       │   │   └── Dockerfile
│       │   ├── tests/
│       │   │   ├── test.sh
│       │   │   ├── verify.py
│       │   │   └── tests.json
│       │   └── solution/
│       │       └── solve.sh
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
- `tests/verify.py` — evaluation logic (for compile + unit test benchmarks)
- `solution/solve.sh` — oracle solution (when available)

## Available Datasets

| Dataset | Tasks | Verification | Parity | Source |
|---|---|---|---|---|
| [harvey-lab](datasets/harvey-lab/) | 1,251 | LLM-as-judge | 25/25 (100%) | [Harvey LAB](https://github.com/harveyai/harvey-labs) |
| [programbench](datasets/programbench/) | 201 | compile + unit tests | 4/5 exact match | [ProgramBench](https://github.com/facebookresearch/programbench) |

## Usage

```bash
# Clone and run with BenchFlow
git clone https://github.com/benchflow-ai/benchmarks.git
cd benchmarks
benchflow run -t datasets/harvey-lab/tasks/<task-id>
benchflow run -t datasets/programbench/tasks/<task-id>

# Or use from the benchflow repo with auto-download
python benchmarks/harvey-lab/run_harvey_lab.py
python benchmarks/run_programbench.py
```

## Adding a Dataset

1. Write a converter in `benchflow-ai/benchflow/benchmarks/<name>/`
2. Run parity tests and record results
3. Generate all tasks and add them under `datasets/<name>/tasks/`
4. Add parity results under `datasets/<name>/parity/`
5. Submit a PR

See [CONVERT.md](https://github.com/benchflow-ai/benchflow/blob/main/benchmarks/CONVERT.md) in the main repo for detailed instructions.

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

## Dataset versions

`registry.json` lists each dataset version in BenchFlow's registry format: every task is pinned to a commit and a content digest, and `bench_version` gives the BenchFlow releases a version needs.

| Dataset | Version | Tasks | BenchFlow (`bench_version`) | Notes |
|---|---|---|---|---|
| programbench | 1.0 | 201 | any | The first conversion (commit `c65af83`), unchanged. **1.0 does not produce scores on any BenchFlow release; use 1.1.** BenchFlow runs test.sh with `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, so the pytest-timeout that 1.0's run.sh installs isn't loaded and every branch scores 0/0. |
| programbench | 1.1 | 201 | `>=0.9.PLACEHOLDER`: the first releases, on the 0.9 and 0.10 lines, that enforce a task's verifier network allowlist (to be filled in) | The verifier reaches only `huggingface.co`, `cas-server.xethub.hf.co`, `us.gcp.cdn.hf.co`, `us.aws.cdn.hf.co`, `pypi.org` and `files.pythonhosted.org`, with pytest-timeout pinned. Hidden tests that are missing or never report end the run unscored (exit 3 or 5), never as a silent 0. Test cases that reach the internet through the program under test aren't counted (`tests/excluded_tests.json`, 1,764 cases in 35 tasks, measured), and two branches whose run.sh can't run under the allowlist aren't run. |

Run a version with `bench run -d programbench@1.0 --registry https://raw.githubusercontent.com/benchflow-ai/benchmarks/main/registry.json`.

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

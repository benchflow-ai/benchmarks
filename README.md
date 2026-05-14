# BenchFlow Benchmarks

Ready-to-run benchmark task directories and parity experiments for [BenchFlow](https://github.com/benchflow-ai/benchflow).

This repo contains **converted tasks** and **parity results** — the output of running each benchmark's converter and validation pipeline. Conversion code, parity tests, and `benchmark.yaml` descriptors live in the main [benchflow](https://github.com/benchflow-ai/benchflow) repo under `benchmarks/<name>/`.

## Structure

```
datasets/
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
- `tests/verify.py` — evaluation logic (compile → anti-cheat → pytest → reward)
- `tests/tests.json` — expected test manifest from ProgramBench
- `solution/solve.sh` — oracle solution (clones original source at commit)

## Available Datasets

| Dataset | Tasks | Languages | Verification | Parity | Source |
|---|---|---|---|---|---|
| [programbench](datasets/programbench/) | 201 | C, Rust, Go, Java, C++ | compile + unit tests | 4/5 exact match | [ProgramBench](https://github.com/facebookresearch/programbench) |

## Usage

```bash
# Clone and run with BenchFlow
git clone https://github.com/benchflow-ai/benchmarks.git
cd benchmarks
benchflow run -t datasets/programbench/tasks/<task-id>

# Or use from the benchflow repo with auto-download
python -m benchmarks.programbench.main
python benchmarks/run_programbench.py
```

## Adding a Dataset

See [CONVERT.md](https://github.com/benchflow-ai/benchflow/blob/main/benchmarks/CONVERT.md) in the main repo.

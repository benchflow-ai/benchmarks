# Program Reconstruction: simeg/eureka

You are given a compiled executable and its documentation.
Your task is to **re-implement the program from scratch** so that your
implementation reproduces the original program's behavior.

## What you have

| Resource | Location |
|----------|----------|
| Compiled executable | `/workspace/executable` |
| Documentation | `/workspace/docs/` (if present) |

Run the executable with `--help` or various inputs to understand its behavior.

## Rules

1. You **must not** decompile or disassemble the executable.
2. You **may** choose any programming language (the original was written in Rust).
3. You **must** create a file called `compile.sh` in `/workspace/` that
   builds your implementation and produces a binary named `executable` in
   the current working directory.
4. You have access to standard development tools installed in the container.

## Deliverables

1. All source code files in `/workspace/`.
2. A build script `/workspace/compile.sh` that, when run, produces
   `./executable`.

## Evaluation

Your implementation will be tested with behavioral tests that compare its
output against the original executable.  Partial credit is awarded based
on the fraction of tests passed.

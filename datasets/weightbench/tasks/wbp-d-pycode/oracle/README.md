# Oracle (withheld)

`solve.sh` and `withheld/` are kept out of git (overlay, kind `withheld-oracle`). `solve.sh` copies
`/oracle/withheld/model.safetensors` (the trained reference weights) to `/app/submission/model.safetensors`.

- **What it is:** the 8-character-context MLP of this task trained by us (116,832 parameters).
- **How it was made:** AdamW (learning rate 2e-3, one-cycle), 4 epochs, batch 1024, on the 1,789 Python files of CPython 3.12.7's `Lib/` directory (32.5 million characters, normalised as in `spec.json`; 2% of the files held back for validation; none of the held-out files is among them), on a 4-CPU Daytona sandbox. The training code (`withheld/train.py`) and its log (`withheld/train.json`)
  are in `withheld/`. Training is ours and is never shown to agents; agents may not train.
- **Score:** 2.117117083 bits per character on the held-out files, reward 1 by definition of the top.

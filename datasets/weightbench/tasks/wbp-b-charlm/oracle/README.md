# Oracle (withheld)

`solve.sh` and `withheld/` are kept out of git (overlay, kind `withheld-oracle`). `solve.sh` copies
`/oracle/withheld/model.safetensors` (the trained reference weights) to `/app/submission/model.safetensors`.

- **What it is:** the 3-character-context MLP of this task trained by us (20,188 parameters).
- **How it was made:** Adam with a one-cycle schedule, 6 epochs, batch 2048, on about 24.5 million characters of 20 public-domain Project Gutenberg novels normalised as in `spec.json` (the held-out novel is not among them), on a 4-CPU Daytona sandbox. The training code (`withheld/train.py`) and its log (`withheld/train.json`)
  are in `withheld/`. Training is ours and is never shown to agents; agents may not train.
- **Score:** 2.325339003 bits per character on the held-out text, reward 1 by definition of the top.

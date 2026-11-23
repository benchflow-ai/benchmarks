# Oracle (withheld)

`solve.sh` and `withheld/` are kept out of git (overlay, kind `withheld-oracle`). `solve.sh` copies
`/oracle/withheld/model.safetensors` (the trained reference weights) to `/app/submission/model.safetensors`.

- **What it is:** the 1-D CNN of this task trained by us (6,774 parameters).
- **How it was made:** AdamW (learning rate 3e-3, one-cycle, weight decay 1e-3), 80 epochs, batch 64, on the 6,243 training windows of 18 of the 21 training volunteers (the other 3, 1,109 windows, for validation), on a CPU virtual machine. The training code (`withheld/train.py`) and its log (`withheld/train.json`)
  are in `withheld/`. Training is ours and is never shown to agents; agents may not train.
- **Score:** held-out accuracy 0.874448592, reward 1 by definition of the top.

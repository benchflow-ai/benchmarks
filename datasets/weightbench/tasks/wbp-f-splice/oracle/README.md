# Oracle (withheld)

`solve.sh` and `withheld/` are kept out of git (overlay, kind `withheld-oracle`). `solve.sh` copies
`/oracle/withheld/model.safetensors` (the trained reference weights) to `/app/submission/model.safetensors`.

- **What it is:** the 320-128-32-2 MLP of this task trained by us (45,282 parameters).
- **How it was made:** AdamW (learning rate 2e-3, one-cycle, weight decay 1e-4), 20 epochs, batch 256, on 476,496 windows from genes on the other chromosomes (half real sites, half consensus-matched decoys, drawn as for the held-out set; 25,078 held back for validation), on a CPU virtual machine. The training code (`withheld/train.py`) and its log (`withheld/train.json`)
  are in `withheld/`. Training is ours and is never shown to agents; agents may not train.
- **Score:** held-out accuracy 0.85375, reward 1 by definition of the top.

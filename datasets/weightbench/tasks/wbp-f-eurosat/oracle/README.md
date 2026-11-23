# Oracle (withheld)

`solve.sh` and `withheld/` are kept out of git (overlay, kind `withheld-oracle`). `solve.sh` copies
`/oracle/withheld/model.safetensors` (the trained reference weights) to `/app/submission/model.safetensors`.

- **What it is:** the small CNN of this task trained by us (38,954 parameters).
- **How it was made:** AdamW (learning rate 3e-3, one-cycle, weight decay 5e-4), 40 epochs, batch 128, random flips and quarter turns, on 21,850 of the 23,000 patches outside the held-out sample (1,150 held back for validation), on a CPU virtual machine. The training code (`withheld/train.py`) and its log (`withheld/train.json`)
  are in `withheld/`. Training is ours and is never shown to agents; agents may not train.
- **Score:** held-out accuracy 0.91075, reward 1 by definition of the top.

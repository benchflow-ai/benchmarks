# Oracle (withheld)

`solve.sh` and `withheld/` are kept out of git (overlay, kind `withheld-oracle`). `solve.sh` copies
`/oracle/withheld/model.safetensors` (the trained reference weights) to `/app/submission/model.safetensors`.

- **What it is:** the 54-128-64-7 MLP of this task trained by us (15,751 parameters).
- **How it was made:** AdamW (learning rate 3e-3, one-cycle), 80 epochs, batch 512, on 511,012 of the 531,012 cells outside the held-out sample (20,000 held back for validation), on a 4-CPU Daytona sandbox. The training code (`withheld/train.py`) and its log (`withheld/train.json`)
  are in `withheld/`. Training is ours and is never shown to agents; agents may not train.
- **Score:** held-out accuracy 0.8997, reward 1 by definition of the top.

# Oracle (withheld)

`solve.sh` and `withheld/` are kept out of git (overlay, kind `withheld-oracle`). `solve.sh` copies
`/oracle/withheld/model.safetensors` (the trained reference weights) to `/app/submission/model.safetensors`.

- **What it is:** the LeNet-5 style CNN of this task trained by us (61,706 parameters).
- **How it was made:** AdamW (learning rate 2e-3, one-cycle), 12 epochs, batch 256, on 290,000 of 300,000 drawings (30,000 per class, drawn from the published bitmaps and disjoint from the held-out set; 10,000 held back for validation), on a 4-CPU Daytona sandbox. The training code (`withheld/train.py`) and its log (`withheld/train.json`)
  are in `withheld/`. Training is ours and is never shown to agents; agents may not train.
- **Score:** held-out accuracy 0.9641, reward 1 by definition of the top.

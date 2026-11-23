# Oracle (withheld)

`solve.sh` and `withheld/` are kept out of git (overlay, kind `withheld-oracle`). `solve.sh` copies
`/oracle/withheld/model.safetensors` (the trained reference weights) to `/app/submission/model.safetensors`.

- **What it is:** the 773-128-32-2 MLP of this task trained by us (103,266 parameters).
- **How it was made:** AdamW (learning rate 2e-3, one-cycle, weight decay 1e-4), 6 epochs, batch 1,024, on 559,428 positions selected in the same way and disjoint from the held-out ones (half per class; 20,000 held back for validation), on a CPU virtual machine. The training code (`withheld/train.py`) and its log (`withheld/train.json`)
  are in `withheld/`. Training is ours and is never shown to agents; agents may not train.
- **Score:** held-out accuracy 0.853, reward 1 by definition of the top.

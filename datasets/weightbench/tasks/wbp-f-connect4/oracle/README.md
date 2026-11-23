# Oracle (withheld)

`solve.sh` and `withheld/` are kept out of git (overlay, kind `withheld-oracle`). `solve.sh` copies
`/oracle/withheld/model.safetensors` (the trained reference weights) to `/app/submission/model.safetensors`.

- **What it is:** the 84-64-32-3 MLP of this task trained by us (7,619 parameters).
- **How it was made:** AdamW (learning rate 3e-3, one-cycle, weight decay 1e-4), 120 epochs, batch 128, class-weighted cross-entropy (inverse class frequency), on 61,330 of the 64,557 positions outside the held-out set (3,227 held back for validation), on a CPU virtual machine. The training code (`withheld/train.py`) and its log (`withheld/train.json`)
  are in `withheld/`. Training is ours and is never shown to agents; agents may not train.
- **Score:** held-out accuracy 0.733666667, reward 1 by definition of the top.

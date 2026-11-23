# Oracle (withheld)

`solve.sh` and `withheld/` are kept out of git (overlay, kind `withheld-oracle`). `solve.sh` copies
`/oracle/withheld/model.safetensors` (the trained reference weights) to `/app/submission/model.safetensors`.

- **What it is:** the 120-64-32-4 MLP of this task trained by us (9,956 parameters).
- **How it was made:** AdamW (learning rate 2e-3, one-cycle, weight decay 1e-4), 60 epochs, batch 256, class-weighted cross-entropy (inverse class frequency), on 92,891 of the 97,780 beats outside the held-out sample (4,889 held back for validation), on a CPU virtual machine. The training code (`withheld/train.py`) and its log (`withheld/train.json`)
  are in `withheld/`. Training is ours and is never shown to agents; agents may not train.
- **Score:** held-out balanced accuracy 0.956666667, reward 1 by definition of the top.

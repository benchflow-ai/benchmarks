# Oracle (withheld)

`solve.sh` and `withheld/` are kept out of git (overlay, kind `withheld-oracle`). `solve.sh` copies
`/oracle/withheld/model.safetensors` (the trained reference weights) to `/app/submission/model.safetensors`.

- **What it is:** the 315-128-64-3 window MLP of this task trained by us (48,899 parameters).
- **How it was made:** AdamW (learning rate 2e-3, one-cycle, weight decay 1e-4), 4 epochs, batch 1,024 residues, on the 6.5 million residues of 25,332 other cluster representatives (516 held back for validation), on a CPU virtual machine. The training code (`withheld/train.py`) and its log (`withheld/train.json`)
  are in `withheld/`. Training is ours and is never shown to agents; agents may not train.
- **Score:** held-out Q3 0.68816294, reward 1 by definition of the top.

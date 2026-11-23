# Oracle (withheld)

`solve.sh` and `withheld/` are kept out of git (overlay, kind `withheld-oracle`). `solve.sh` copies
`/oracle/withheld/model.safetensors` (the trained reference weights) to `/app/submission/model.safetensors`.

- **What it is:** the trigram bag-of-features model of this task trained by us (203,820 parameters).
- **How it was made:** AdamW (learning rate 1e-2, one-cycle, weight decay 1e-4), 6 epochs, batch 64, on 57,000 of the 60,000 training sentences (5,000 per language, disjoint from the held-out ones; 3,000 held back for validation), on a 4-CPU Daytona sandbox. The training code (`withheld/train.py`) and its log (`withheld/train.json`)
  are in `withheld/`. Training is ours and is never shown to agents; agents may not train.
- **Score:** held-out accuracy 0.915666667, reward 1 by definition of the top.

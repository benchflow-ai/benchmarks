# Oracle (withheld)

`solve.sh` and `withheld/` are kept out of git (overlay, kind `withheld-oracle`). `solve.sh` copies
`/oracle/withheld/model.safetensors` (the trained reference weights) to `/app/submission/model.safetensors`.

- **What it is:** the small CNN of this task trained by us (37,354 parameters).
- **How it was made:** AdamW (learning rate 3e-3, one-cycle, weight decay 5e-4), 40 epochs, batch 128, random horizontal flips and 4-pixel crops, on the first 45,000 CIFAR-10 training images (5,000 held back for validation; no test image used), on a 4-CPU Daytona sandbox. The training code (`withheld/train.py`) and its log (`withheld/train.json`)
  are in `withheld/`. Training is ours and is never shown to agents; agents may not train.
- **Score:** test accuracy 0.733, reward 1 by definition of the top.

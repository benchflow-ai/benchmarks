# Oracle (withheld)

`solve.sh` and `withheld/` are kept out of git (overlay, kind `withheld-oracle`). `solve.sh` copies
`/oracle/withheld/model.safetensors` (the trained reference weights) to `/app/submission/model.safetensors`.

- **What it is:** the LeNet-5 style CNN of this task trained by us (61,706 parameters).
- **How it was made:** AdamW (learning rate 2e-3, one-cycle), 20 epochs, batch 256, on 57,000 of the 60,000 Fashion-MNIST training images (3,000 held back for validation; no test image used), on a CPU virtual machine. The training code (`withheld/train.py`) and its log (`withheld/train.json`)
  are in `withheld/`. Training is ours and is never shown to agents; agents may not train.
- **Score:** test accuracy 0.902, reward 1 by definition of the top.

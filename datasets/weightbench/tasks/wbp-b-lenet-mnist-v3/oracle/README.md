# Oracle (withheld)

`solve.sh` and `withheld/` are kept out of git (overlay, kind `withheld-oracle`). `solve.sh` copies
`/oracle/withheld/model.safetensors` (the trained reference weights) to `/app/submission/model.safetensors`.

- **What it is:** the LeNet-5 style CNN of this task trained by us (61,706 parameters).
- **How it was made:** Adam (learning rate 1e-3, cosine decay), 15 epochs, batch 128, on the first 55,000 MNIST training images (5,000 held back for validation; no test image used), on a 4-CPU Daytona sandbox. The training code (`withheld/train.py`) and its log (`withheld/train.json`)
  are in `withheld/`. Training is ours and is never shown to agents; agents may not train.
- **Score:** test accuracy 0.9915, reward 1 by definition of the top.

# Oracle (withheld)

`solve.sh` and `withheld/` are kept out of git (overlay, kind `withheld-oracle`). `solve.sh` copies
`/oracle/withheld/model.safetensors` (the trained reference weights) to `/app/submission/model.safetensors`.

- **What it is:** the small CNN of this task trained by us (36,554 parameters).
- **How it was made:** AdamW (learning rate 3e-3, one-cycle, weight decay 5e-4), 40 epochs, batch 128, random time shifts of up to 5 frames, on the 30,769 training clips of the ten words (the official validation list, 3,703 clips, for validation; no test clip used), on a CPU virtual machine. The training code (`withheld/train.py`) and its log (`withheld/train.json`)
  are in `withheld/`. Training is ours and is never shown to agents; agents may not train.
- **Score:** held-out accuracy 0.960235641, reward 1 by definition of the top.

# Oracle (withheld)

`solve.sh` and `withheld/` are kept out of git (overlay, kind `withheld-oracle`). `solve.sh` copies
`/oracle/withheld/model.safetensors` (the trained reference weights) to `/app/submission/model.safetensors`.

- **What it is:** the 4-note-context MLP of this task trained by us (7,246 parameters).
- **How it was made:** AdamW (learning rate 3e-3, one-cycle), 60 epochs, batch 128, the best of three weight-decay settings by validation loss, on the melodies of 268 of the 298 training chorales (30 held back for validation), on a 4-CPU Daytona sandbox. The training code (`withheld/train.py`) and its log (`withheld/train.json`)
  are in `withheld/`. Training is ours and is never shown to agents; agents may not train.
- **Score:** 2.407573646 bits per note on the held-out melodies, reward 1 by definition of the top.

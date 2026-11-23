# Oracle (withheld)

`solve.sh` and `withheld/` are kept out of git (overlay, kind `withheld-oracle`). `solve.sh` copies
`/oracle/withheld/model.safetensors` (the trained reference weights) to `/app/submission/model.safetensors`.

- **What it is:** the 105-64-32-1 MLP of this task trained by us (8,897 parameters).
- **How it was made:** AdamW (learning rate 2e-3, one-cycle), 300 epochs, batch 64, mean squared error on standardised inputs (the scaling folded into fc1 afterwards), weight decay chosen from 1e-4, 1e-3 and 1e-2 on a validation tenth, on 7,632 of the 8,480 compounds outside the held-out set, on a CPU virtual machine. The training code (`withheld/train.py`) and its log (`withheld/train.json`)
  are in `withheld/`. Training is ours and is never shown to agents; agents may not train.
- **Score:** held-out MSE 1.50558628, reward 1 by definition of the top.

# Forward computation (wbp-f-ss3)

For residue i of a chain s (0-based), the input is a window of 15 positions, p = 0..14 covering residues i-7 .. i+7.
Each position contributes 21 values: a one-hot over the symbols ACDEFGHIKLMNPQRSTVWY (index 0..19) and "other"
(index 20, any other letter); a position beyond either end of the chain contributes 21 zeros.

    x[21 * p + k] = 1 if residue i - 7 + p exists and has symbol k, else 0      # 315 values
    h1 = relu(fc1.weight @ x + fc1.bias)        # 128
    h2 = relu(fc2.weight @ h1 + fc2.bias)       # 64
    logits = fc3.weight @ h2 + fc3.bias         # 3: 0 helix (H), 1 strand (E), 2 coil (C)

The prediction is the argmax (tie rule below). The metric is the share of residues of all held-out chains predicted
correctly. Layouts are PyTorch [out, in].

The verifier computes this in float64 from your float32 tensors. A float32 pass is recorded only.

Argmax tie rule (the verifier's, so that an exact tie is broken the same way on every CPU): logits within
1e-9 x max(1, |max logit|) of the row maximum count as tied, and ties go to the lowest index.

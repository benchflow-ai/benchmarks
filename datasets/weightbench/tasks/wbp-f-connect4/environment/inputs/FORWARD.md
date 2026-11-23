# Forward computation (wbp-f-connect4)

For one position, x is 84 values (`spec.json` encoding): x[c] = 1 if the first player x has a piece on cell c,
x[42 + c] = 1 if o has one, with c = 6 * column + (row - 1) (column a = 0 .. g = 6, row 1 at the bottom).

    h1 = relu(fc1.weight @ x + fc1.bias)        # 64
    h2 = relu(fc2.weight @ h1 + fc2.bias)       # 32
    logits = fc3.weight @ h2 + fc3.bias         # 3: 0 win, 1 draw, 2 loss, for x with perfect play

The prediction is the argmax (tie rule below). Layouts are PyTorch [out, in].

The verifier computes this in float64 from your float32 tensors. A float32 pass is recorded only.

Argmax tie rule (the verifier's, so that an exact tie is broken the same way on every CPU): logits within
1e-9 x max(1, |max logit|) of the row maximum count as tied, and ties go to the lowest index.

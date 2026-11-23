# Forward computation (wbp-b-charlm)

Alphabet (28 symbols), index i is the i-th character of `" .abcdefghijklmnopqrstuvwxyz"`: 0 is the space, 1 the full stop,
2..27 are `a`..`z`.

For each position i of the normalised text t (0-based), the context is (t[i-3], t[i-2], t[i-1]), with the
space (index 0) standing in for positions before the start of the text. With c1, c2, c3 the context's
indices, oldest first:

    x      = concat(emb[c1], emb[c2], emb[c3])                  # 3 x 16 = 48 values
    h      = tanh(hidden.weight @ x + hidden.bias)               # 256
    logits = out.weight @ h + out.bias                           # 28
    p      = softmax(logits)                                     # exp(logits - max) / sum(exp(logits - max))
    bits_i = -log2 p[t[i]]

The metric is the mean of bits_i over every position of the held-out text. Tensor layout: `emb` is
[28, 16] (row = symbol), `hidden.weight` is [256, 48] (PyTorch [out, in]), `out.weight` is [28, 256].

The verifier computes this in float64 from your float32 tensors. A float32 pass is recorded only.

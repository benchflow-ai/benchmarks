# Forward computation (wbp-d-pycode)

Symbols (96): index 0 is the newline, index 1 + k is the character chr(32 + k) for k = 0..94 (space, `!`, ... `~`).
Files are normalised first (`spec.json` normalization_python: CRLF and CR become newlines, a tab becomes four
spaces, any other character outside the 96 is dropped).

For each position i of a normalised file t (0-based), the context is (t[i-8], ..., t[i-1]), with the newline
(index 0) standing in for positions before the start of the file. With c1 .. c8 the context's indices, oldest
first:

    x      = concat(emb[c1], emb[c2], ..., emb[c8])              # 8 x 16 = 128 values
    h      = tanh(hidden.weight @ x + hidden.bias)               # 512
    logits = out.weight @ h + out.bias                           # 96
    p      = softmax(logits)                                     # exp(logits - max) / sum(exp(logits - max))
    bits_i = -log2 p[t[i]]

The metric is the mean of bits_i over every position of every held-out file. Tensor layout: `emb` is [96, 16]
(row = symbol), `hidden.weight` is [512, 128] (PyTorch [out, in]), `out.weight` is [96, 512].

The verifier computes this in float64 from your float32 tensors. A float32 pass is recorded only.

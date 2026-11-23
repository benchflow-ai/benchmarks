# Forward computation (wbp-d-chorales)

Input symbols (23): index 0 is "start", index 1 + j is MIDI pitch 60 + j (j = 0..21, C4 to A5).
Output classes (22): class j is MIDI pitch 60 + j.

For each note i of a chorale's melody m (0-based), the context is (m[i-4], .., m[i-1]) as input symbols, with
"start" standing in for positions before the first note. With c1 .. c4 the context's indices, oldest first:

    x      = concat(emb[c1], emb[c2], emb[c3], emb[c4])          # 4 x 8 = 32 values
    h      = tanh(hidden.weight @ x + hidden.bias)               # 128
    logits = out.weight @ h + out.bias                           # 22
    p      = softmax(logits)                                     # exp(logits - max) / sum(exp(logits - max))
    bits_i = -log2 p[m[i] - 60]

The metric is the mean of bits_i over every note of every held-out chorale. Tensor layout: `emb` is [23, 8]
(row = input symbol), `hidden.weight` is [128, 32] (PyTorch [out, in]), `out.weight` is [22, 128].

The verifier computes this in float64 from your float32 tensors. A float32 pass is recorded only.

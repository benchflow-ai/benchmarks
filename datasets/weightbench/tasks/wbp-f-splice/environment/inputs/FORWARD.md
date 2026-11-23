# Forward computation (wbp-f-splice)

For one window w of 80 nucleotides (w[0] .. w[79], the sense strand 5' to 3', the candidate GT or AG at w[40], w[41]):

    x[4 * p + b] = 1 if w[p] is base b (b: 0 A, 1 C, 2 G, 3 T), else 0      # 320 values
    h1 = relu(fc1.weight @ x + fc1.bias)        # 128
    h2 = relu(fc2.weight @ h1 + fc2.bias)       # 32
    logits = fc3.weight @ h2 + fc3.bias         # 2: 0 decoy, 1 real splice site

The prediction is the argmax (tie rule below). Layouts are PyTorch [out, in].

The verifier computes this in float64 from your float32 tensors. A float32 pass is recorded only.

Argmax tie rule (the verifier's, so that an exact tie is broken the same way on every CPU): logits within
1e-9 x max(1, |max logit|) of the row maximum count as tied, and ties go to the lowest index.

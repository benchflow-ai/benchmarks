# Forward computation (wbp-d-quickdraw)

Input: one 28 x 28 grey drawing, x[0, i, j] = pixel[i, j] / 255 (row i from the top, column j from the left;
0 is background, 1 is full ink). Classes: 0 airplane, 1 bicycle, 2 cat, 3 clock, 4 envelope, 5 fish, 6 house, 7 star, 8 tree, 9 umbrella.

    a1 = relu(conv(x, conv1.weight, conv1.bias, pad=2))    # [6, 28, 28]
    p1 = maxpool2(a1)                                      # [6, 14, 14]
    a2 = relu(conv(p1, conv2.weight, conv2.bias, pad=0))   # [16, 10, 10]
    p2 = maxpool2(a2)                                      # [16, 5, 5]
    f  = flatten(p2)                                       # 400, index c*25 + i*5 + j
    h1 = relu(fc1.weight @ f + fc1.bias)                   # 120
    h2 = relu(fc2.weight @ h1 + fc2.bias)                  # 84
    logits = fc3.weight @ h2 + fc3.bias                    # 10; prediction = argmax (tie rule below)

- conv(in, W, b, pad): zero-pad `pad` pixels on every side, then
  out[o, i, j] = b[o] + sum over c, u, v of W[o, c, u, v] * in[c, i + u, j + v], u, v in 0..4
  (cross-correlation, as PyTorch `Conv2d`, stride 1).
- maxpool2: the maximum of each non-overlapping 2 x 2 block, stride 2.
- relu(z) = max(z, 0). Weights use the PyTorch layouts: conv [out, in, kh, kw], linear [out, in].

The verifier computes this in float64 from your float32 tensors. A float32 pass is recorded only.

Argmax tie rule (the verifier's, so that an exact tie is broken the same way on every CPU): logits within
1e-9 x max(1, |max logit|) of the row maximum count as tied, and ties go to the lowest index.

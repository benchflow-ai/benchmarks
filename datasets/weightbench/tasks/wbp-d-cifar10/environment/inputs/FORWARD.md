# Forward computation (wbp-d-cifar10)

Input: one 32 x 32 colour photograph, x[c, i, j] = pixel[c, i, j] / 255 (channel c = 0 red, 1 green, 2 blue;
row i from the top, column j from the left). Classes: 0 airplane, 1 automobile, 2 bird, 3 cat, 4 deer, 5 dog, 6 frog, 7 horse, 8 ship, 9 truck.

    a1 = relu(conv(x, conv1.weight, conv1.bias, pad=2))     # [16, 32, 32]
    p1 = maxpool2(a1)                                       # [16, 16, 16]
    a2 = relu(conv(p1, conv2.weight, conv2.bias, pad=2))    # [32, 16, 16]
    p2 = maxpool2(a2)                                       # [32, 8, 8]
    a3 = relu(conv(p2, conv3.weight, conv3.bias, pad=1))    # [64, 8, 8]
    g  = mean of a3 over its 8 x 8 positions                # 64
    h  = relu(fc1.weight @ g + fc1.bias)                    # 64
    logits = fc2.weight @ h + fc2.bias                      # 10; prediction = argmax (tie rule below)

- conv(in, W, b, pad): zero-pad `pad` pixels on every side, then
  out[o, i, j] = b[o] + sum over c, u, v of W[o, c, u, v] * in[c, i + u, j + v], u, v in 0..k-1
  (cross-correlation, as PyTorch `Conv2d`, stride 1; k = 5 for conv1 and conv2, 3 for conv3).
- maxpool2: the maximum of each non-overlapping 2 x 2 block, stride 2.
- relu(z) = max(z, 0). Weights use the PyTorch layouts: conv [out, in, kh, kw], linear [out, in].

The verifier computes this in float64 from your float32 tensors. A float32 pass is recorded only.

Argmax tie rule (the verifier's, so that an exact tie is broken the same way on every CPU): logits within
1e-9 x max(1, |max logit|) of the row maximum count as tied, and ties go to the lowest index.

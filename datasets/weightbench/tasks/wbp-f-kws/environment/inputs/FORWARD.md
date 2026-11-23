# Forward computation (wbp-f-kws)

Input: the [1, 40, 49] log-mel spectrogram of a one-second clip (`spec.json` input: row 0 is the lowest mel band,
column t the frame starting at 20 t ms; 1.0 is the loudest band-frame of the clip, 0.0 is 80 dB below it or quieter;
`features_python` is the exact recipe). Classes: 0 "yes", 1 "no", 2 "up", 3 "down", 4 "left", 5 "right", 6 "on", 7 "off", 8 "stop", 9 "go".

    a1 = relu(conv(x, conv1.weight, conv1.bias, pad=2))     # [16, 40, 49]
    p1 = maxpool2(a1)                                       # [16, 20, 24]
    a2 = relu(conv(p1, conv2.weight, conv2.bias, pad=2))    # [32, 20, 24]
    p2 = maxpool2(a2)                                       # [32, 10, 12]
    a3 = relu(conv(p2, conv3.weight, conv3.bias, pad=1))    # [64, 10, 12]
    g  = maximum of a3 over its 10 x 12 positions           # 64
    h  = relu(fc1.weight @ g + fc1.bias)                    # 64
    logits = fc2.weight @ h + fc2.bias                      # 10; prediction = argmax (tie rule below)

- conv(in, W, b, pad): zero-pad `pad` on every side, then out[o, i, j] = b[o] + sum over c, u, v of
  W[o, c, u, v] * in[c, i + u, j + v] (cross-correlation, as PyTorch `Conv2d`, stride 1).
- maxpool2: the maximum of each non-overlapping 2 x 2 block, stride 2; an odd last row or column is dropped.
- relu(z) = max(z, 0). Layouts: conv [out, in, kh, kw], linear [out, in].

The verifier computes this in float64 from your float32 tensors. A float32 pass is recorded only.

Argmax tie rule (the verifier's, so that an exact tie is broken the same way on every CPU): logits within
1e-9 x max(1, |max logit|) of the row maximum count as tied, and ties go to the lowest index.

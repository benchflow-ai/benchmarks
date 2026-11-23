# Forward computation (wbp-f-eurosat)

Input: one 640 x 640 m patch, x[c, i, j] for band c (0 B02 blue 490 nm, 1 B03 green 560 nm, 2 B04 red 665 nm, 3 B05
red edge 705 nm, 4 B08 near infrared 842 nm, 5 B11 short-wave infrared 1610 nm, 6 B12 short-wave infrared 2190 nm),
row i (north at the top) and column j: top-of-atmosphere reflectance (`spec.json` input). Classes: 0 AnnualCrop, 1 Forest, 2 HerbaceousVegetation, 3 Highway, 4 Industrial, 5 Pasture, 6 PermanentCrop, 7 Residential, 8 River, 9 SeaLake.

    a1 = relu(conv(x, conv1.weight, conv1.bias, pad=2))     # [16, 32, 32]
    p1 = maxpool2(a1)                                       # [16, 16, 16]
    a2 = relu(conv(p1, conv2.weight, conv2.bias, pad=2))    # [32, 16, 16]
    p2 = maxpool2(a2)                                       # [32, 8, 8]
    a3 = relu(conv(p2, conv3.weight, conv3.bias, pad=1))    # [64, 8, 8]
    g  = mean of a3 over its 8 x 8 positions                # 64
    h  = relu(fc1.weight @ g + fc1.bias)                    # 64
    logits = fc2.weight @ h + fc2.bias                      # 10; prediction = argmax (tie rule below)

- conv(in, W, b, pad): zero-pad `pad` on every side, then out[o, i, j] = b[o] + sum over c, u, v of
  W[o, c, u, v] * in[c, i + u, j + v] (cross-correlation, as PyTorch `Conv2d`, stride 1).
- maxpool2: the maximum of each non-overlapping 2 x 2 block, stride 2. relu(z) = max(z, 0).
- The zero padding means that beyond the patch's edge every band reads 0 (no reflectance): a filter that responds
  to brightness also responds along the borders.
- Layouts: conv [out, in, kh, kw], linear [out, in].

The verifier computes this in float64 from your float32 tensors. A float32 pass is recorded only.

Argmax tie rule (the verifier's, so that an exact tie is broken the same way on every CPU): logits within
1e-9 x max(1, |max logit|) of the row maximum count as tied, and ties go to the lowest index.

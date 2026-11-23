# Forward computation (wbp-f-har)

Input: x[6, 128], channels total_acc_x, total_acc_y, total_acc_z (g, gravity included), body_gyro_x, body_gyro_y,
body_gyro_z (rad/s), 128 samples at 50 Hz.

    a1 = relu(conv1d(x, conv1.weight, conv1.bias, pad=4))   # [16, 128]
    p1 = maxpool2(a1)                                       # [16, 64]
    a2 = relu(conv1d(p1, conv2.weight, conv2.bias, pad=4))  # [32, 64]
    p2 = maxpool2(a2)                                       # [32, 32]
    g  = mean of p2 over its 32 time steps                  # 32
    h  = relu(fc1.weight @ g + fc1.bias)                    # 32
    logits = fc2.weight @ h + fc2.bias                      # 6; prediction = argmax (tie rule below)

- conv1d(in, W, b, pad): zero-pad `pad` steps at each end, then out[o, t] = b[o] + sum over c, u of
  W[o, c, u] * in[c, t + u], u = 0..8 (cross-correlation, as PyTorch `Conv1d`, stride 1).
- maxpool2: the maximum of each non-overlapping pair of steps, stride 2.
- Classes: 0 walking, 1 walking upstairs, 2 walking downstairs, 3 sitting, 4 standing, 5 lying. Layouts: conv [out, in, k], linear [out, in].

The verifier computes this in float64 from your float32 tensors. A float32 pass is recorded only.

Argmax tie rule (the verifier's, so that an exact tie is broken the same way on every CPU): logits within
1e-9 x max(1, |max logit|) of the row maximum count as tied, and ties go to the lowest index.

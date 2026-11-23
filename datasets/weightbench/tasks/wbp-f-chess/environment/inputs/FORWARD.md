# Forward computation (wbp-f-chess)

For one position (a FEN: pieces, side to move, castling rights), x is 773 values (`spec.json` encoding_python):

    x[64 * piece + 8 * rank + file] = 1 for each piece on the board   # piece order P N B R Q K p n b r q k,
                                                                       # rank and file 0..7 (a1 = square 0)
    x[768] = 1 if White is to move                                     # else 0
    x[769 .. 772] = castling rights K, Q, k, q                         # 1 if still held
    h1 = relu(fc1.weight @ x + fc1.bias)        # 128
    h2 = relu(fc2.weight @ h1 + fc2.bias)       # 32
    logits = fc3.weight @ h2 + fc3.bias         # 2: 0 Black is better, 1 White is better

The prediction is the argmax (tie rule below). Layouts are PyTorch [out, in].

The verifier computes this in float64 from your float32 tensors. A float32 pass is recorded only.

Argmax tie rule (the verifier's, so that an exact tie is broken the same way on every CPU): logits within
1e-9 x max(1, |max logit|) of the row maximum count as tied, and ties go to the lowest index.

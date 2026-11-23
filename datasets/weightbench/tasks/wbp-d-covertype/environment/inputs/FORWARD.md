# Forward computation (wbp-d-covertype)

For one 30 x 30 m cell, x is the 54 features of `spec.json` (`features`, index 0..53): ten measurements under fixed
unit conversions (elevation and distances in kilometres, aspect and slope as fractions of 360 and 90 degrees,
hillshade as a fraction of 255; not bounded to [0, 1]: a distance can exceed 1 km and the height above water can be
negative), four 0/1 wilderness indicators and forty 0/1 soil-type indicators.

    h1 = relu(fc1.weight @ x + fc1.bias)        # 128
    h2 = relu(fc2.weight @ h1 + fc2.bias)       # 64
    logits = fc3.weight @ h2 + fc3.bias         # 7; prediction = argmax (tie rule below)

Class k is cover type k + 1: 0 Spruce/Fir, 1 Lodgepole Pine, 2 Ponderosa Pine, 3 Cottonwood/Willow, 4 Aspen,
5 Douglas-fir, 6 Krummholz. Layouts are PyTorch [out, in].

The verifier computes this in float64 from your float32 tensors. A float32 pass is recorded only.

Argmax tie rule (the verifier's, so that an exact tie is broken the same way on every CPU): logits within
1e-9 x max(1, |max logit|) of the row maximum count as tied, and ties go to the lowest index.

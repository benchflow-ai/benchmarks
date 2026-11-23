# Forward computation (wbp-f-ecg)

For one beat, x is 120 values (`spec.json` inputs): 117 samples of lead MLII in millivolts, baseline removed, from
250 ms before the annotated R peak to about 397 ms after it at 180 samples per second (the R peak falls between
x[44] and x[45]), then three RR intervals in seconds: before the beat (x[117]), after it (x[118]), the local mean
of the up to 10 most recent intervals, ending with x[117] (x[119]).

    h1 = relu(fc1.weight @ x + fc1.bias)        # 64
    h2 = relu(fc2.weight @ h1 + fc2.bias)       # 32
    logits = fc3.weight @ h2 + fc3.bias         # 4; prediction = argmax (tie rule below)

Classes: 0 N (normal and bundle branch block beats), 1 S (supraventricular ectopic), 2 V (ventricular ectopic), 3 F (fusion of ventricular and normal). Layouts are PyTorch [out, in]. The metric is the mean of the four per-class recalls.

The verifier computes this in float64 from your float32 tensors. A float32 pass is recorded only.

Argmax tie rule (the verifier's, so that an exact tie is broken the same way on every CPU): logits within
1e-9 x max(1, |max logit|) of the row maximum count as tied, and ties go to the lowest index.

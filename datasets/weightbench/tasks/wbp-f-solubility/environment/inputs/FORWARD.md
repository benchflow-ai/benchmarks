# Forward computation (wbp-f-solubility)

For one compound, x is the 105 features of `spec.json` (`features`, index 0..104): RDKit's 85 fragment counts,
atom counts by element, ring, donor, acceptor and rotatable-bond counts, the fraction of sp3 carbons, the total
absolute formal charge, the number of disconnected parts and the molecular weight / 100.

    h1 = relu(fc1.weight @ x + fc1.bias)        # 64
    h2 = relu(fc2.weight @ h1 + fc2.bias)       # 32
    prediction = fc3.weight @ h2 + fc3.bias     # 1: predicted log10(solubility in mol/L)

Layouts are PyTorch [out, in]. The prediction is used as it is (not clipped or rounded).

The verifier computes this in float64 from your float32 tensors. A float32 pass is recorded only.

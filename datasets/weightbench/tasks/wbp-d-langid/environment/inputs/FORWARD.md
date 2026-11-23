# Forward computation (wbp-d-langid)

For one sentence:

    t      = normalize(sentence)                   # spec.json normalization_python (adds one space at each end)
    grams  = [t[i:i+3] for i in range(len(t) - 2)]
    rows   = [vocab_index[g] for g in grams if g in vocab_index]   # repeats kept, unknown trigrams dropped
    h      = mean(embedding[r] for r in rows)                      # 16 values; zeros if rows is empty
    logits = fc.weight @ h + fc.bias                               # 12
    class  = argmax(logits)                                        # tie rule below

`vocab_index[g]` is the 0-based line number of g in `vocab.txt` (12726 lines). Classes: 0 Spanish, 1 Portuguese, 2 Galician, 3 Catalan, 4 Danish, 5 Norwegian Bokmål, 6 Norwegian Nynorsk, 7 Swedish, 8 Czech, 9 Slovak, 10 Indonesian, 11 Malay (Standard Malay). Layouts:
`embedding` [12726, 16] (row = trigram), `fc.weight` [12, 16] (PyTorch [out, in]).

The verifier computes this in float64 from your float32 tensors (sum of rows, then divided by their number).
A float32 pass is recorded only.

Argmax tie rule (the verifier's, so that an exact tie is broken the same way on every CPU): logits within
1e-9 x max(1, |max logit|) of the row maximum count as tied, and ties go to the lowest index.

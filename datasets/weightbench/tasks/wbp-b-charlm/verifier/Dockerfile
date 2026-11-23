# WeightBench pilot (family b) verifier: CPU, no network. Canonical float64 NumPy forward pass.
FROM python:3.12-slim-bookworm@sha256:935c3c5b12357a7e10caa9c1e6ca5692344d97cf229832ef584be2cec9fc03df
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 \
    OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 OPENBLAS_CORETYPE=Haswell \
    NPY_DISABLE_CPU_FEATURES="AVX512F AVX512CD AVX512_KNL AVX512_KNM AVX512_SKX AVX512_CLX AVX512_CNL AVX512_ICL AVX512_SPR"
RUN apt-get update && apt-get install -y --no-install-recommends procps iptables \
 && rm -rf /var/lib/apt/lists/*
RUN pip install numpy==2.2.6 safetensors==0.5.3
WORKDIR /app

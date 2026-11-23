# WeightBench native-001 BERT verifier: CPU GLUE evaluation, no network.
# Package versions are those of the pass3 evaluator image (en305-small-evaluator:003,
# sha256:777952b6bf49a70101385329d269c6d0160c0af4b72f8c0a6ec7e256d2028cbc); proof/prove_bert.py shows
# this image reproduces pass3 points.
FROM python:3.12-slim-bookworm@sha256:935c3c5b12357a7e10caa9c1e6ca5692344d97cf229832ef584be2cec9fc03df
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 \
    OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 TOKENIZERS_PARALLELISM=false HF_HUB_OFFLINE=1
RUN pip install --index-url https://download.pytorch.org/whl/cpu torch==2.6.0+cpu \
 && pip install numpy==2.2.6 safetensors==0.5.3 tokenizers==0.22.2 huggingface_hub==0.36.2 transformers==4.57.1
WORKDIR /app

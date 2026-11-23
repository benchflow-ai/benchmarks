# WeightBench native-001 Qwen verifier: schema check on CPU, grading on Modal's A100 (modal_grader.py).
FROM python:3.12-slim-bookworm@sha256:935c3c5b12357a7e10caa9c1e6ca5692344d97cf229832ef584be2cec9fc03df
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1
RUN pip install --index-url https://download.pytorch.org/whl/cpu torch==2.14.0+cpu \
 && pip install numpy==2.5.4 safetensors==0.8.0 modal==1.6.3
WORKDIR /app

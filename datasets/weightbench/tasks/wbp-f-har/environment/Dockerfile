# WeightBench pilot (family f): the writer's sandbox. Python with numpy and safetensors, the task's inputs and a
# schema checker. No model, no dataset, no simulator. iptables is preinstalled for BenchFlow's no-network guard.
FROM python:3.12-slim-bookworm@sha256:935c3c5b12357a7e10caa9c1e6ca5692344d97cf229832ef584be2cec9fc03df
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1
RUN apt-get update && apt-get install -y --no-install-recommends procps iptables && rm -rf /var/lib/apt/lists/*
RUN pip install numpy==2.2.6 safetensors==0.5.3
COPY inputs /app/inputs
COPY check_submission.py /app/tools/check_submission.py
RUN chmod -R a+rX,a-w /app/inputs /app/tools && mkdir -p /app/submission /app/work && chmod 0777 /app/submission /app/work
WORKDIR /app

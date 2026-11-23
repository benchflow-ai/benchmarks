# WeightBench native-001, BERT-tiny target: the writer's sandbox.
# The agent (user `agent`, created by BenchFlow) gets Python with numpy and safetensors, the schema,
# configuration and vocabulary, and a schema checker. No torch, no transformers, no GLUE data, no
# weights. iptables is preinstalled for BenchFlow's no-network guard.
FROM python:3.12-slim-bookworm@sha256:935c3c5b12357a7e10caa9c1e6ca5692344d97cf229832ef584be2cec9fc03df
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1
RUN apt-get update && apt-get install -y --no-install-recommends procps iptables && rm -rf /var/lib/apt/lists/*
RUN pip install numpy==2.2.6 safetensors==0.5.3
COPY inputs /app/inputs
COPY check_submission.py /app/tools/check_submission.py
RUN chmod -R a+rX,a-w /app/inputs /app/tools && mkdir -p /app/submission /app/work && chmod 0777 /app/submission /app/work
WORKDIR /app

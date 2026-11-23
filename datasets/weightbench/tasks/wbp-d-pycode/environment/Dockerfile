# WeightBench pilot (family d): the writer's sandbox. Python with numpy and safetensors, the task's inputs and a
# schema checker. No model, no dataset, no simulator. iptables is preinstalled for BenchFlow's no-network guard.
FROM python:3.12-slim-bookworm@sha256:935c3c5b12357a7e10caa9c1e6ca5692344d97cf229832ef584be2cec9fc03df
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1
RUN apt-get update && apt-get install -y --no-install-recommends procps iptables && rm -rf /var/lib/apt/lists/*
RUN pip install numpy==2.2.6 safetensors==0.5.3
# This task scores a model of Python source code, so the image keeps no Python source text: every .py file of the
# Python installation (standard library and site-packages) is compiled to bytecode in place and deleted, and the
# gcc and gdb debugger helper scripts of the base image are removed. Imports still work from the .pyc files;
# tracebacks show no source lines.
RUN python3 -m compileall -q -b -f -j 0 /usr/local/lib/python3.12 >/dev/null \
 && find /usr/local/lib/python3.12 -name "*.py" -delete \
 && find /usr/local/lib/python3.12 -name __pycache__ -type d -prune -exec rm -rf {} + \
 && rm -rf /usr/share/gcc/python /usr/share/gdb/auto-load \
 && python3 -c "import json, re, math, numpy, safetensors.numpy" \
 && test -z "$(find / -xdev -name '*.py' -not -path '/proc/*' 2>/dev/null | head -1)"
COPY inputs /app/inputs
COPY check_submission.py /app/tools/check_submission.py
RUN chmod -R a+rX,a-w /app/inputs /app/tools && mkdir -p /app/submission /app/work && chmod 0777 /app/submission /app/work
WORKDIR /app

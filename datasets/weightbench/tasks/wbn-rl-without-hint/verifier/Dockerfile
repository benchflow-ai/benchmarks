# WeightBench native-001 classic-control verifier: the frozen pass3 evaluator (en305-small-evaluator:003,
# sha256:777952b6bf49...) rebuilt from its recorded layers: Python 3.12.16, torch 2.6.0+cpu, numpy 2.2.6,
# safetensors 0.5.3, gymnasium 1.2.2, one thread.
FROM python:3.12.16-slim-trixie
ENV PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 \
    OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
RUN pip install --index-url https://download.pytorch.org/whl/cpu torch==2.6.0+cpu \
 && pip install numpy==2.2.6 safetensors==0.5.3 gymnasium==1.2.2
WORKDIR /app

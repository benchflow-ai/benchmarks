FROM python:3.13-slim

RUN apt-get update -qq && apt-get install -y -qq \
    pandoc \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    pdfplumber \
    openpyxl \
    python-docx \
    python-pptx \
    markitdown \
    pandas \
    google-genai

WORKDIR /app

# Copy task documents
COPY documents/ /app/documents/

# Copy rubric for the verifier
COPY rubric.json /app/rubric.json

RUN mkdir -p /logs/verifier /logs/agent /logs/artifacts

FROM programbench/ismaelgv_1776_rnr.fc0733b:task

WORKDIR /workspace

# Reset workspace to cleanroom state: wipe source, keep binary + assets.
# ProgramBench eval does the same: start from :task, wipe workspace,
# extract agent submission, then compile.
RUN rm -rf /workspace/.git /workspace/src /workspace/Cargo.* /workspace/Makefile* \
           /workspace/CMakeLists.txt /workspace/configure* /workspace/meson* \
           /workspace/*.c /workspace/*.h /workspace/*.rs /workspace/*.go \
           /workspace/*.java /workspace/*.hs /workspace/*.cabal /workspace/go.* \
           /workspace/pom.xml /workspace/build.gradle /workspace/setup.py \
           /workspace/pyproject.toml /workspace/package.json 2>/dev/null; true
# Re-initialize a clean git repo (matches cleanroom's single "Initial commit")
RUN cd /workspace && git init -q && git add -A && \
    git -c user.email=clean@local -c user.name=clean commit -q --allow-empty -m 'Initial commit' 2>/dev/null; true

# BenchFlow log directories
RUN mkdir -p /logs/verifier /logs/agent /logs/artifacts

# Verification dependencies — the verifier downloads test archives from
# HuggingFace and runs pytest suites against the agent's executable.
RUN apt-get update -qq && \
    apt-get install -y -qq python3 python3-pip git jq && \
    rm -rf /var/lib/apt/lists/* 2>/dev/null; true

RUN pip3 install --quiet huggingface_hub pyyaml junitparser || \
    pip3 install --break-system-packages --quiet huggingface_hub pyyaml junitparser

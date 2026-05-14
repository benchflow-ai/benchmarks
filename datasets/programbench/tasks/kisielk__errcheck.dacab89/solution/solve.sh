#!/bin/bash
# Oracle solution: check out the original source code from the upstream repo.
# The task asks agents to reconstruct the program from a compiled binary —
# the gold answer is the original source at the specified commit.
set -euo pipefail

cd /workspace

# Clone the original repository and check out the exact commit
git clone https://github.com/kisielk/errcheck.git _oracle_src
cd _oracle_src
git checkout dacab891ef4a1c38ecf6c4d94fd66746bb1247d5
cd /workspace

# Copy source into workspace (overwriting the cleanroom state)
cp -a _oracle_src/. .
rm -rf _oracle_src .git

# Run the existing compile.sh to produce the executable
if [ -f compile.sh ]; then
    chmod +x compile.sh
    bash compile.sh
fi

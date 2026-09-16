#!/usr/bin/env bash
set -euo pipefail

# Set these once; they are reused for every benchmark.
# You can also export them before calling this script to override.
export MODEL_NAME="${MODEL_NAME:-mymodel}"
export URL="${URL:-http://localhost:8000/}"
export VERSION="${VERSION:-}"

# Use the repo's virtualenv if it exists.
AIPERF="aiperf"
[ -x .venv/bin/aiperf ] && AIPERF=".venv/bin/aiperf"

run() {
  local config="$1"
  echo ">> ${config}.yaml  (MODEL_NAME=${MODEL_NAME}, URL=${URL}, VERSION=${VERSION})"
  "$AIPERF" profile --ui simple --gpu-telemetry pynvml --config "benchmark_configs/${config}.yaml"
}

# All configs, in order. Override with arguments, e.g. ./run.sh minimal simple_chat
configs=("minimal" "simple_chat" "api_calls" "coding_agent")

if [ "$#" -gt 0 ]; then
  for c in "$@"; do run "$c"; done
else
  for c in "${configs[@]}"; do run "$c"; done
fi

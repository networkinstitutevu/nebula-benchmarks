#!/usr/bin/env bash
set -e

MODEL="Inferact/Qwen3.8-27B-NVFP4"          # match your NIM
TOKENIZER="Inferact/Qwen3.8-27B-NVFP4"
URL="http://localhost:8000/vllm"
MEASUREMENT_INTERVAL=500                  # ms per measurement window
REQUEST_COUNT=400
WARMUP=10
CONCURRENCY=100
name="simple_chat"
isl=300
is_std=150
osl=200

echo "=== ${name} | ISL=${isl} OSL=${osl} | concurrency=${CONCURRENCY} ==="
aiperf profile \
    -m "$MODEL" \
    --ui-type dashboard \
    --endpoint-type chat \
    --url "$URL" \
    --streaming \
    --gpu-telemetry pynvml \
    --synthetic-input-tokens-mean "$isl" \
    --synthetic-input-tokens-stddev "$is_std" \
    --output-tokens-mean "$osl" \
    --extra-inputs max_tokens:$((osl * 2)) \
    --tokenizer "$TOKENIZER" \
    --concurrency "$CONCURRENCY" \
    --stats-interval "$MEASUREMENT_INTERVAL" \
    --request-count "$REQUEST_COUNT" \
    --warmup-request-count "$WARMUP" \
    --random-seed 42 \
    --profile-export-file "artifacts/prod_bench_${name}_isl${isl}_osl${osl}_c${CONCURRENCY}.json" \

#!/usr/bin/env bash
set -e

MODEL="RedHatAI/gemma-4-31B-it-NVFP4"          # match your NIM
TOKENIZER="RedHatAI/gemma-4-31B-it-NVFP4"
URL="http://localhost:8000/vllm"
MEASUREMENT_INTERVAL=500                  # ms per measurement window
REQUEST_COUNT=100
WARMUP=20



run_profile() {
    local name="$1" isl="$2" is_std="$3" osl="$4"
    for CONCURRENCY in 10 25 50 75 100 150 200; do
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
    done
}

run_profile simple_chat   300  150 200
run_profile api_calls     200  100 100
run_profile coding_agent 10000 2000 1000

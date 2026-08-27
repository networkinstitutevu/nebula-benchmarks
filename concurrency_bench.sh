for c in 10 50 100 200 500; do
  aiperf profile 
    --model "meta-llama/Llama-3.1-8B-Instruct" \
    --url http://145.108.224.12/llama/ \
    --endpoint-type chat \
    --tokenizer meta-llama/Llama-3.1-8B-Instruct \
    --streaming
    --concurrency $c \
    --request-count 1000 \
    --isl 1000 \
    --osl 500 \
    --artifact-dir "artifacts/pareto-c$c"
done

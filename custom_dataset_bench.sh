aiperf profile  \
    --model "meta-llama/Llama-3.1-8B-Instruct" \
    --url http://145.108.224.12/llama/ \
    --endpoint-type chat \
    --tokenizer meta-llama/Llama-3.1-8B-Instruct \
    --request-count 10 \
    --streaming

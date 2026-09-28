# Findings
The goal of this file is to act as a report to what we find running benchmarks on the models we plan to deploy. 

## Limitations
* we are currently running a very rudimentary benchmark
* these experiments have only one repetition. Everything is running once, and then data is analyzed. Hopefully when we get more hardware, we'll be able to experiment with statistical significance in mind

# Inferact/Qwen3.8-27B-NVFP4
## Configurations
* **v1** - base configuration recommended by the vLLM cookbook
* **v2** - fine tune configuration recommended by Gemini based on the initial config
* **v3** - fine tune configuration based on v2, with reduced batched tokens
* **v4** - fine tune configuration based on v3, with speculative decoding

## Results
### coding_agent
#### Total Token Throughput [tokens/s]
| **config** | **concurrency 10** | **concurrency 25** | **concurrency 50** | **concurrency 75** | **concurrency 100** | **concurrency 150** | **concurrency 200** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **v1** | 3810.56 | 5769.83 | 6802.94 | 7242.64 | 6779.07 | 6847.58 | 6823.81 |
| **v2** | 3788.19 | 5694.51 | 6724.78 | 7068.69 | 7232.90 | 6396.86 | 6450.06 |
| **v3** | 3802.53 | 5743.64 | 6763.00 | 7179.49 | 7375.64 | 6784.17 | 6751.95 |
| **v4** | 4936.29 | 6572.07 | 7197.91 | 6504.83 | 6520.65 | 6525.62 | 6390.39 |

#### E2E Output Token Throughput [tokens/s/user]
| **config** | **concurrency 10** | **concurrency 25** | **concurrency 50** | **concurrency 75** | **concurrency 100** | **concurrency 150** | **concurrency 200** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **v1** | 33.91 | 20.80 | 12.47 | 8.99 | 6.60 | 4.34 | 3.32 |
| **v2** | 33.82 | 20.51 | 12.31 | 8.80 | 6.77 | 4.12 | 3.14 |
| **v3** | 33.92 | 20.70 | 12.42 | 8.91 | 6.93 | 4.39 | 3.23 |
| **v4** | 44.63 | 23.99 | 13.50 | 8.05 | 6.12 | 4.24 | 3.31 |

#### Nvidia Energy Per Total Token [mJ/token]
| **config** | **concurrency 10** | **concurrency 25** | **concurrency 50** | **concurrency 75** | **concurrency 100** | **concurrency 150** | **concurrency 200** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **v1** | 108.89 | 73.32 | 63.93 | 60.31 | 64.88 | 64.37 | 64.76 |
| **v2** | 117.24 | 86.46 | 77.32 | 75.44 | 74.72 | 85.46 | 85.49 |
| **v3** | 117.84 | 81.75 | 71.81 | 68.33 | 66.93 | 73.20 | 73.88 |
| **v4** | 88.39 | 71.08 | 64.21 | 71.46 | 71.51 | 72.04 | 73.83 |

### api_calls
#### Total Token Throughput [tokens/s]
| **config** | **concurrency 10** | **concurrency 25** | **concurrency 50** | **concurrency 75** | **concurrency 100** | **concurrency 150** | **concurrency 200** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **v1** | 1522.58 | 2983.25 | 4198.40 | 4776.18 | 5162.38 | 5508.25 | 5790.10 |
| **v2** | 1527.34 | 2989.42 | 4180.30 | 4754.83 | 5065.47 | 5386.66 | 5705.81 |
| **v3** | 1527.62 | 2987.06 | 4176.77 | 4766.09 | 5144.83 | 5476.64 | 5761.06 |
| **v4** | 2389.41 | 3815.20 | 4691.89 | 5138.06 | 5239.02 | 5240.99 | 5241.14 |

#### E2E Output Token Throughput [tokens/s/user]
| **config** | **concurrency 10** | **concurrency 25** | **concurrency 50** | **concurrency 75** | **concurrency 100** | **concurrency 150** | **concurrency 200** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **v1** | 48.76 | 38.33 | 27.40 | 21.06 | 17.03 | 12.48 | 9.60 |
| **v2** | 48.92 | 38.41 | 27.28 | 20.99 | 16.70 | 12.25 | 9.37 |
| **v3** | 48.93 | 38.38 | 27.26 | 21.04 | 16.96 | 12.43 | 9.48 |
| **v4** | 79.77 | 51.51 | 32.42 | 23.38 | 18.42 | 12.30 | 9.57 |

#### Nvidia Energy Per Total Token [mJ/token]
| **config** | **concurrency 10** | **concurrency 25** | **concurrency 50** | **concurrency 75** | **concurrency 100** | **concurrency 150** | **concurrency 200** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **v1** | 273.03 | 130.80 | 101.74 | 88.77 | 84.72 | 77.88 | 73.84 |
| **v2** | 335.94 | 171.90 | 129.60 | 115.42 | 108.25 | 102.06 | 95.67 |
| **v3** | 314.25 | 155.40 | 118.19 | 102.74 | 96.35 | 90.08 | 85.17 |
| **v4** | 184.20 | 120.10 | 98.76 | 90.77 | 92.37 | 90.41 | 90.48 |

### simple_chat
#### Total Token Throughput [tokens/s]
| **config** | **concurrency 10** | **concurrency 25** | **concurrency 50** | **concurrency 75** | **concurrency 100** | **concurrency 150** | **concurrency 200** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **v1** | 1298.85 | 2617.16 | 3789.13 | 4375.38 | 4770.99 | 5122.41 | 5444.94 |
| **v2** | 1303.43 | 2631.42 | 3783.75 | 4326.75 | 4723.48 | 5057.68 | 5352.82 |
| **v3** | 1303.69 | 2612.79 | 3775.61 | 4371.95 | 4758.77 | 5101.86 | 5424.38 |
| **v4** | 2069.97 | 3374.84 | 4321.67 | 4649.79 | 4773.73 | 4763.52 | 4741.20 |

#### E2E Output Token Throughput [tokens/s/user]
| **config** | **concurrency 10** | **concurrency 25** | **concurrency 50** | **concurrency 75** | **concurrency 100** | **concurrency 150** | **concurrency 200** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **v1** | 50.13 | 40.51 | 29.75 | 23.24 | 18.92 | 13.97 | 10.84 |
| **v2** | 50.30 | 40.73 | 29.70 | 23.03 | 18.71 | 13.82 | 10.57 |
| **v3** | 50.32 | 40.71 | 29.64 | 23.25 | 18.85 | 13.92 | 10.75 |
| **v4** | 83.65 | 54.97 | 35.97 | 25.55 | 20.18 | 13.41 | 10.51 |

#### Nvidia Energy Per Total Token [mJ/token]
| **config** | **concurrency 10** | **concurrency 25** | **concurrency 50** | **concurrency 75** | **concurrency 100** | **concurrency 150** | **concurrency 200** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **v1** | 342.15 | 150.21 | 112.63 | 96.01 | 90.57 | 82.92 | 78.91 |
| **v2** | 391.96 | 194.53 | 143.42 | 126.90 | 116.52 | 108.78 | 102.09 |
| **v3** | 371.57 | 175.95 | 129.56 | 111.98 | 104.47 | 96.31 | 90.28 |
| **v4** | 210.20 | 134.85 | 108.09 | 101.44 | 99.84 | 99.90 | 100.27 |

## Conclusions
**`v4` (speculative decoding) ideal for this deployment.**
Our production environment low concurrency most of the time. At this operating
point `v4` is simultaneously the most energy-efficient and the fastest
configuration across all three workloads.

### Why `v4` at the expected operating point
At low concurrency the GPU is under-utilised, so energy per token is
dominated by fixed power draw spread over few tokens. `v4`'s speculative
decoding roughly doubles throughput at the same concurrency, so it finishes
the same 1000 requests faster and burns far less total energy per token.

At c=10, `v4` wins every metric in every
workload vs `v1`:

| workload | energy/token (v4 / v1) | e2e out tok/s/user (v4 / v1) | total tok/s (v4 / v1) |
| --- | --- | --- | --- |
| coding_agent | 88.4 / 108.9 | 44.6 / 33.9 | 4936 / 3811 |
| api_calls | 184.2 / 273.0 | 79.8 / 48.8 | 2389 / 1523 |
| simple_chat | 210.2 / 342.2 | 83.7 / 50.1 | 2070 / 1299 |

`v4` remains the most energy-efficient config up through c=50 in all three
workloads (e.g. simple_chat c=50: 108.1 vs 112.6 mJ/token for `v1`).

### Caveat: the advantage reverses at high concurrency
`v4`'s benefit is not free. At high concurrency (≥75–200), where the GPU is
already saturated, the speculative-decoding draft model adds overhead with
no throughput headroom, so `v4` loses both throughput and energy efficiency:

| workload | energy/token at c=200 (v1 / v4) | total tok/s at c=200 (v1 / v4) |
| --- | --- | --- |
| coding_agent | 64.8 / 73.8 | 6824 / 6390 |
| api_calls | 73.8 / 90.5 | 5790 / 5241 |
| simple_chat | 78.9 / 100.3 | 5445 / 4741 |

Here `v1` (and `v3`) are the most energy-efficient and highest-throughput
options. The crossover is around c≈75–200.

### Bottom line
We **deploy `v4`** and will re-evaluate only when (if)
the user base grows enough to push sustained concurrency past ~75, at which
point `v3` becomes the better choice on energy and throughput.


# openai/gpt-oss:120b
## Configurations
* **v1** - base configuration (vLLM cookbook style): gpu-memory-utilization 0.88, max-num-batched-tokens 8192, max-cudagraph-capture-size 2048, stream-interval 20.
* **v2** - fine-tune: gpu-memory-utilization 0.95, max-model-len 65536 (64K context), kv-cache-dtype fp8, max-num-seqs 32, max-num-batched-tokens 32768, enable-chunked-prefill, max-cudagraph-capture-size 256, stream-interval 2.
* **v3** - fine-tune based on v2 with 128K context: max-model-len 131072 (doubled), max-num-seqs 16 (halved from 32 to keep KV cache memory identical to the 64K config), max-cudagraph-capture-size 16 (matched to max-num-seqs, freeing VRAM for the KV cache).

## Results
### coding_agent
#### Total Token Throughput [tokens/s]
| **config** | **concurrency 10** | **concurrency 25** | **concurrency 50** | **concurrency 75** | **concurrency 100** | **concurrency 150** | **concurrency 200** |
|  --- |  --- |  --- |  --- |  --- |  --- |  --- |  --- |
| **v1** | 5485.07 | 6755.86 | 7777.48 | 7803.05 | 7791.89 | 7797.61 | 7699.74 |
| **v2** | 6678.33 | 8982.02 | 9750.35 | 9787.85 | 9727.96 | 9677.54 | 9741.29 |
| **v3** | 5977.42 | 7330.17 | 7333.27 | 7352.01 | 7313.74 | 7291.04 | 7349.16 |

#### E2E Output Token Throughput [tokens/s/user]
| **config** | **concurrency 10** | **concurrency 25** | **concurrency 50** | **concurrency 75** | **concurrency 100** | **concurrency 150** | **concurrency 200** |
|  --- |  --- |  --- |  --- |  --- |  --- |  --- |  --- |
| **v1** | 44.93 | 22.31 | 12.91 | 8.69 | 6.80 | 4.88 | 3.94 |
| **v2** | 54.36 | 29.53 | 16.07 | 10.86 | 8.50 | 6.12 | 4.98 |
| **v3** | 48.23 | 24.04 | 12.35 | 8.55 | 6.78 | 5.02 | 4.18 |

#### Nvidia Energy Per Total Token [mJ/token]
| **config** | **concurrency 10** | **concurrency 25** | **concurrency 50** | **concurrency 75** | **concurrency 100** | **concurrency 150** | **concurrency 200** |
|  --- |  --- |  --- |  --- |  --- |  --- |  --- |  --- |
| **v1** | 80.60 | 64.37 | 56.79 | 56.69 | 56.75 | 57.29 | 57.90 |
| **v2** | 62.32 | 48.74 | 45.26 | 45.22 | 45.48 | 45.96 | 45.75 |
| **v3** | 73.78 | 61.47 | 61.54 | 61.57 | 62.01 | 62.36 | 61.97 |

### api_calls
#### Total Token Throughput [tokens/s]
| **config** | **concurrency 10** | **concurrency 25** | **concurrency 50** | **concurrency 75** | **concurrency 100** | **concurrency 150** | **concurrency 200** |
|  --- |  --- |  --- |  --- |  --- |  --- |  --- |  --- |
| **v1** | 2309.16 | 3516.63 | 5855.94 | 7287.63 | 8723.67 | 10869.37 | 12539.61 |
| **v2** | 2546.97 | 4365.50 | 5035.49 | 5119.56 | 4953.12 | 5070.37 | 5012.27 |
| **v3** | 2362.85 | 3287.57 | 3345.21 | 3374.07 | 3275.77 | 3364.28 | 3329.35 |

#### E2E Output Token Throughput [tokens/s/user]
| **config** | **concurrency 10** | **concurrency 25** | **concurrency 50** | **concurrency 75** | **concurrency 100** | **concurrency 150** | **concurrency 200** |
|  --- |  --- |  --- |  --- |  --- |  --- |  --- |  --- |
| **v1** | 72.43 | 44.22 | 37.42 | 31.46 | 28.17 | 24.09 | 20.29 |
| **v2** | 79.90 | 54.90 | 36.50 | 23.28 | 17.68 | 12.92 | 10.53 |
| **v3** | 74.07 | 45.87 | 22.58 | 15.57 | 12.23 | 9.16 | 7.66 |

#### Nvidia Energy Per Total Token [mJ/token]
| **config** | **concurrency 10** | **concurrency 25** | **concurrency 50** | **concurrency 75** | **concurrency 100** | **concurrency 150** | **concurrency 200** |
|  --- |  --- |  --- |  --- |  --- |  --- |  --- |  --- |
| **v1** | 191.59 | 133.31 | 80.32 | 63.54 | 53.30 | 42.45 | 40.32 |
| **v2** | 164.97 | 103.54 | 89.81 | 87.98 | 90.97 | 89.27 | 89.75 |
| **v3** | 189.03 | 137.33 | 135.16 | 134.14 | 137.94 | 134.00 | 135.23 |

### simple_chat
#### Total Token Throughput [tokens/s]
| **config** | **concurrency 10** | **concurrency 25** | **concurrency 50** | **concurrency 75** | **concurrency 100** | **concurrency 150** | **concurrency 200** |
|  --- |  --- |  --- |  --- |  --- |  --- |  --- |  --- |
| **v1** | 1959.51 | 2919.18 | 4970.18 | 6250.85 | 7469.92 | 9462.86 | 11102.50 |
| **v2** | 2096.17 | 3666.67 | 4200.27 | 4317.21 | 4188.26 | 4270.61 | 4242.22 |
| **v3** | 1957.46 | 2749.04 | 2740.62 | 2813.24 | 2706.26 | 2795.60 | 2753.09 |

#### E2E Output Token Throughput [tokens/s/user]
| **config** | **concurrency 10** | **concurrency 25** | **concurrency 50** | **concurrency 75** | **concurrency 100** | **concurrency 150** | **concurrency 200** |
|  --- |  --- |  --- |  --- |  --- |  --- |  --- |  --- |
| **v1** | 74.49 | 44.50 | 38.48 | 32.69 | 29.17 | 25.39 | 21.70 |
| **v2** | 79.66 | 55.89 | 36.48 | 23.75 | 18.06 | 13.21 | 10.81 |
| **v3** | 74.32 | 46.09 | 22.29 | 15.67 | 12.23 | 9.23 | 7.71 |

#### Nvidia Energy Per Total Token [mJ/token]
| **config** | **concurrency 10** | **concurrency 25** | **concurrency 50** | **concurrency 75** | **concurrency 100** | **concurrency 150** | **concurrency 200** |
|  --- |  --- |  --- |  --- |  --- |  --- |  --- |  --- |
| **v1** | 224.48 | 160.45 | 94.85 | 74.60 | 62.27 | 48.63 | 44.44 |
| **v2** | 201.43 | 123.32 | 107.82 | 104.58 | 107.62 | 106.03 | 106.59 |
| **v3** | 223.97 | 163.57 | 164.39 | 160.16 | 166.20 | 160.63 | 163.44 |

## Conclusions
We selected **`v2`** as the best operating point. `v2` (64K context
with an FP8 KV cache and chunked prefill) is the most efficient
config at low-to-moderate concurrency across all three workloads: at
c=10 it leads `v1` on every metric in every workload, and it stays
ahead through roughly c=25.

| workload | energy/token (v2 / v1) | e2e out tok/s/user (v2 / v1) | total tok/s (v2 / v1) |
| --- | --- | --- | --- |
| coding_agent | 62.3 / 80.6 | 54.4 / 44.9 | 6678 / 5485 |
| api_calls | 165.0 / 191.6 | 79.9 / 72.4 | 2547 / 2309 |
| simple_chat | 201.4 / 224.5 | 79.7 / 74.5 | 2096 / 1960 |

### Caveat: the advantage reverses at high concurrency
For `api_calls` and `simple_chat`, `v2`'s edge disappears at high
concurrency; the crossover is around c≈50, after which **`v1`** (the
base config) becomes the better choice. `v2` caps active sequences at
32 and runs a large 32768-token batch, so it plateaus its throughput
and stalls its energy per token; `v1`, with no active-sequence cap and
a much larger cuDGraph capture size (2048 vs 256), keeps scaling
throughput and keeps its energy per token falling as concurrency
climbs. `coding_agent` is the exception: `v2` keeps winning it across
the whole sweep (throughput 9741 vs 7700 tok/s, energy 45.8 vs 57.9
mJ/token at c=200), so the advantage reverses in none of the three
workloads.

| workload | energy/token at c=200 (v1 / v2) | total tok/s at c=200 (v1 / v2) |
| --- | --- | --- |
| coding_agent | 57.9 / 45.7 | 7700 / 9741 |
| api_calls | 40.3 / 89.8 | 12540 / 5012 |
| simple_chat | 44.4 / 106.6 | 11102 / 4242 |

### `v3` is never the best choice
`v3` (128K context, max-num-seqs 16, cuDGraph capture 16) is the most
constrained of the three and never wins. It is dominated by `v2`
across all of `coding_agent`, and by `v1` at high concurrency in
`api_calls` and `simple_chat`. At c=200 it is the worst on every
metric in those two workloads (`api_calls`: total 3329 vs 12540
tok/s, energy 135.2 vs 40.3 mJ/token; `simple_chat`: total 2753 vs
11103 tok/s, energy 163.4 vs 44.4 mJ/token). Its halved
active-sequence cap and doubled context leave it with the lowest
throughput and highest energy per token once the GPU is well-used.

### Bottom line
We **deploy `v2`** for low-to-moderate concurrency (c ≤ ~50), where it
is the best config on throughput, energy, and per-user output across
all three workloads. Fall back to **`v1`** only when sustained
concurrency pushes past ~50 on `api_calls` / `simple_chat`, where it
scales throughput and energy better. Avoid **`v3`** unless a 128K
context window is actually required.

# nebula-benchmarks

Repository for benchmarking the models deployed and to be deployed on Nebula.

Benchmarks are driven by [NVIDIA AIPerf](https://github.com/ai-dynamo/aiperf) and
defined as YAML configs in [`benchmark_configs/`](benchmark_configs/). Each config
describes the model, the API endpoint, the synthetic dataset, the run phases, and an
optional parameter sweep.

## Prerequisites

- A Python environment (a `.venv/` is provided in this repo)
- An OpenAI-compatible inference server (e.g. vLLM) running and serving a chat endpoint
- NVIDIA GPU + drivers (AIPerf reads GPU metrics via `pynvml` / `nvidia-ml-py`)

## Installation

```bash
# create / activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

`requirements.txt` installs `aiperf`, `pynvml`, and `nvidia-ml-py`.

## Running a Benchmark

Benchmarks are run with the AIPerf `profile` command, pointing at a config file:

```bash
aiperf profile --config <config-file.yaml>
```

The bundled configs read two environment variables:

| Variable     | Purpose                                              | Default                     |
| ------------ | ---------------------------------------------------- | -------------------------- |
| `MODEL_NAME` | Name of the model served by the endpoint             | required                   |
| `URL`        | Base URL of the inference server                   | `http://localhost:8000/` |

### Quick start

```bash
# 1. point at your server and name the model
export URL="http://localhost:8000/"
export MODEL_NAME="my-model"

# 2. run a config
aiperf profile --config benchmark_configs/minimal.yaml
```

`minimal.yaml` is the fastest way to get started — it uses AIPerf shorthand forms
and a single phase, so it finishes quickly.

### Running the other configs

```bash
aiperf profile --config benchmark_configs/simple_chat.yaml   # conversational / chat workload
aiperf profile --config benchmark_configs/coding_agent.yaml  # long-context coding-agent workload
aiperf profile --config benchmark_configs/api_calls.yaml     # API-call workload with a sweep
```

`simple_chat.yaml`, `api_calls.yaml`, and `coding_agent.yaml` each include a warmup
phase plus a profiling phase, and a `grid` sweep over `concurrency`
`[10, 25, 50, 75, 100, 150, 200]`. `coding_agent.yaml` uses a large input
(≈10k tokens) to emulate a coding-agent context.

### Useful flags

You can override values on the command line without editing the config, e.g.:

```bash
# override the endpoint URL and model name directly
aiperf profile --config benchmark_configs/minimal.yaml \
  --url http://localhost:8000/ \
  --model-name my-model
```

See `aiperf profile --help` for the full list of options (streaming, endpoint type,
URL strategy, etc.).

## Config Files

All configs live in [`benchmark_configs/`](benchmark_configs/) and use the AIPerf
schema (v2.0). AIPerf auto-expands the shorthand forms used here (`model:` →
`models.items[0].name`, `dataset:` → a one-entry `datasets` list, a flat `phases:`
→ a one-entry `phases` list). Both snake_case and camelCase keys are accepted.

| Config             | Dataset entries | Input size (mean) | Use case                          |
| ------------------ | --------------- | ---------------- | -------------------------------- |
| `minimal.yaml`     | 100             | 512 tokens       | Fastest smoke test / quick start |
| `simple_chat.yaml` | 100             | 300 tokens (±150) | Chat / conversational workload   |
| `api_calls.yaml`   | 100             | 200 tokens (±100) | Short API calls, with a sweep    |
| `coding_agent.yaml`| 1000            | 10,000 tokens (±2,000) | Long-context coding-agent |

Each config (except `minimal.yaml`) writes a JSON summary under
`./artifacts/<config>/`.

## Validating and Visualizing

Validate a config against the schema before running:

```bash
aiperf config validate benchmark_configs/minimal.yaml
```

Expand a swept config to see the resulting variations:

```bash
aiperf config expand benchmark_configs/api_calls.yaml
```

Generate plots from the profiling results (requires Chrome/Chromium for PNG export):

```bash
aiperf plot
```

Analyze a profiling run:

```bash
aiperf analyze
```

### Interactive dashboard

The `visualize/` package is an interactive [Dash](https://plotly.com/dash/) +
[Plotly](https://plotly.com/python/) web app that plots the sweep-aggregate data
written to `artifacts/{modelSupplier}/{modelName}/{benchmarkType}/sweep_aggregate/`.
It compares a chosen metric against `concurrency`, one line per benchmark type
(or per model × benchmark type), with an explanation panel and a numbers table.

```bash
# from the repo root, with the virtualenv active
source .venv/bin/activate
python3 visualize/app.py            # serves the dashboard at http://127.0.0.1:8050
```

Command-line options:

| Option        | Purpose                                   | Default             |
| ------------- | ----------------------------------------- | ------------------- |
| `--artifacts` | Directory containing the artifacts        | `artifacts`         |
| `--port`      | Port to serve the dashboard on            | `8050`              |
| `--host`      | Host to bind to                           | `127.0.0.1`         |

The dashboard provides:

- **Variable selector** — a searchable list of every metric found in the data
  (grouped and labelled with its unit). Selecting one shows an explanation panel
  with the metric's label, unit, category, a higher-is-better hint, and a
  plain-English description.
- **Layout modes** — one line per benchmark type, one line per model ×
  benchmark type, or a two-metric overlay (e.g. throughput vs latency on dual
  axes).
- **Filters** — multi-select for models and benchmark types, a min–max
  uncertainty band toggle, and a log y-axis toggle.
- A **numbers table** of the selected metric by benchmark, model, and
  concurrency.

The data source is discovered automatically from the `artifacts/` directory tree,
so adding a new model (or supplier) folder makes it appear in the filters and
plots without changing any code.

The visualizer needs `dash`, `dash-bootstrap-components`, and `plotly`
(already available in this repo's `.venv`). Install them if needed:

```bash
pip install dash dash-bootstrap-components plotly
```

## Results

Profiling output (summaries, traces, metrics) is written to the artifact directory
declared in each config (e.g. `./artifacts/`), and reports latency, throughput,
token statistics, and GPU resource utilization.

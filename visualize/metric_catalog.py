"""Human-readable catalog of AIPerf sweep metrics.

Provides curated labels, units, categories, explanations and a
higher-is-better hint for the metrics that matter most, plus a
auto-generated fallback for any metric found in the data but not listed
here, so the variable dropdown stays complete and modular as new metrics
or models are added.
"""

from __future__ import annotations

CATEGORY_ORDER = [
    "throughput",
    "latency",
    "tokens",
    "efficiency",
    "gpu",
    "http",
    "misc",
]

METRIC_INFO: dict[str, dict[str, str]] = {
    "request_throughput": {
        "unit": "requests/sec",
        "category": "throughput",
        "higher_is_better": "yes",
        "description": "Number of complete requests processed per second across the whole server. The headline end-to-end throughput: higher means the system serves more users per second.",
    },
    "request_latency": {
        "unit": "ms",
        "category": "latency",
        "higher_is_better": "no",
        "description": "Mean wall-clock time from a request being issued to its full response, including queueing and generation. Lower is better; it grows as the server approaches saturation.",
    },
    "effective_latency": {
        "unit": "ms",
        "category": "latency",
        "higher_is_better": "no",
        "description": "Latency measured only over the active (effective) portion of the run, excluding warm-up/credit time. A cleaner per-request latency than request_latency.",
    },
    "time_to_first_token": {
        "unit": "ms",
        "category": "latency",
        "higher_is_better": "no",
        "description": "Time-to-first-token (TTFT): latency from request start to the first output token. The dominant term for perceived 'interactivity'; lower feels more responsive.",
    },
    "time_to_second_token": {
        "unit": "ms",
        "category": "latency",
        "higher_is_better": "no",
        "description": "Latency from the first output token to the second token. Roughly the time to start streaming; lower is better.",
    },
    "inter_token_latency": {
        "unit": "ms",
        "category": "latency",
        "higher_is_better": "no",
        "description": "Mean time between consecutive output tokens while generating (the decode/typing speed). Lower gives smoother, faster streaming; it is the inverse of per-token speed.",
    },
    "inter_chunk_latency": {
        "unit": "ms",
        "category": "latency",
        "higher_is_better": "no",
        "description": "Mean time between streamed response chunks. Close to inter_token_latency but measured at the chunk level; lower is better for smooth streaming.",
    },
    "credit_to_start_latency": {
        "unit": "ms",
        "category": "latency",
        "higher_is_better": "no",
        "description": "Latency from when the client is 'credited' (time sent to the server) to when work actually starts. Captures queueing/scheduling delay before generation begins.",
    },
    "decode_duration": {
        "unit": "ms",
        "category": "latency",
        "higher_is_better": "no",
        "description": "Mean time spent in the decode phase (generating output tokens). Part of request_latency; lower is generally better for a fixed output length.",
    },
    "output_token_throughput": {
        "unit": "tokens/sec",
        "category": "throughput",
        "higher_is_better": "yes",
        "description": "Total output tokens generated per second by the server. The primary generation-throughput metric; higher means the model produces more text per second.",
    },
    "output_token_throughput_per_user": {
        "unit": "tokens/sec/user",
        "category": "throughput",
        "higher_is_better": "yes",
        "description": "Output tokens per second per concurrent user. Normalises throughput by the number of users, so it is the fairest 'speed per user' comparison across concurrency levels.",
    },
    "e2e_output_token_throughput": {
        "unit": "tokens/sec/user",
        "category": "throughput",
        "higher_is_better": "yes",
        "description": "End-to-end output-token throughput per user, measured across the whole request lifetime. The user-facing streaming speed; higher is better.",
    },
    "active_decode_throughput": {
        "unit": "tokens/sec",
        "category": "throughput",
        "higher_is_better": "yes",
        "description": "Output (decode) tokens per second during the active profiling window. Reflects raw generation speed while the GPU is busy.",
    },
    "active_decode_throughput_per_user": {
        "unit": "tokens/sec/user",
        "category": "throughput",
        "higher_is_better": "yes",
        "description": "Active decode throughput normalised per user. Per-user generation speed during the active window; higher is better.",
    },
    "active_prefill_throughput": {
        "unit": "tokens/sec",
        "category": "throughput",
        "higher_is_better": "yes",
        "description": "Input (prefill) tokens processed per second during the active window. Higher means prompt processing is faster, which lowers time-to-first-token.",
    },
    "active_prefill_throughput_per_user": {
        "unit": "tokens/sec/user",
        "category": "throughput",
        "higher_is_better": "yes",
        "description": "Active prefill throughput normalised per user. Per-user prompt-processing speed; higher is better.",
    },
    "effective_decode_throughput": {
        "unit": "tokens/sec",
        "category": "throughput",
        "higher_is_better": "yes",
        "description": "Decode throughput measured only over the effective (active) window, excluding warm-up. A clean generation-throughput figure.",
    },
    "effective_prefill_throughput": {
        "unit": "tokens/sec",
        "category": "throughput",
        "higher_is_better": "yes",
        "description": "Prefill throughput over the effective window. Higher means prompts are processed faster in steady state.",
    },
    "effective_total_throughput": {
        "unit": "tokens/sec",
        "category": "throughput",
        "higher_is_better": "yes",
        "description": "Combined input + output token throughput over the effective window. The overall token-processing rate of the server.",
    },
    "effective_decode_throughput_per_user": {
        "unit": "tokens/sec/user",
        "category": "throughput",
        "higher_is_better": "yes",
        "description": "Effective decode throughput per user. Per-user generation speed in steady state; higher is better.",
    },
    "effective_prefill_throughput_per_user": {
        "unit": "tokens/sec/user",
        "category": "throughput",
        "higher_is_better": "yes",
        "description": "Effective prefill throughput per user. Per-user prompt-processing speed in steady state; higher is better.",
    },
    "active_total_throughput": {
        "unit": "tokens/sec",
        "category": "throughput",
        "higher_is_better": "yes",
        "description": "Total (input + output) token throughput during the active window. The overall token-processing rate while the GPU is busy.",
    },
    "total_token_throughput": {
        "unit": "tokens/sec",
        "category": "throughput",
        "higher_is_better": "yes",
        "description": "Sum of input and output tokens processed per second. The server's overall token throughput; higher is better.",
    },
    "input_token_throughput": {
        "unit": "tokens/sec",
        "category": "throughput",
        "higher_is_better": "yes",
        "description": "Input (prompt) tokens processed per second. Higher means the prompt/long-context phase is faster.",
    },
    "effective_concurrency": {
        "unit": "requests",
        "category": "throughput",
        "higher_is_better": "neutral",
        "description": "Average number of requests actually being processed at once (vs. the target concurrency). Reveals how much of the requested concurrency the server could sustain.",
    },
    "effective_decode_concurrency": {
        "unit": "requests",
        "category": "throughput",
        "higher_is_better": "neutral",
        "description": "Average number of requests in the decode (generation) phase at once. Indicates how many generations run in parallel.",
    },
    "effective_prefill_concurrency": {
        "unit": "requests",
        "category": "throughput",
        "higher_is_better": "neutral",
        "description": "Average number of requests in the prefill (prompt) phase at once. Shows how many prompts are processed in parallel.",
    },
    "tokens_in_flight": {
        "unit": "tokens",
        "category": "tokens",
        "higher_is_better": "neutral",
        "description": "Average number of tokens currently being generated/processed at once (batch depth). Higher batch depth usually raises throughput but can increase latency.",
    },
    "input_sequence_length": {
        "unit": "tokens",
        "category": "tokens",
        "higher_is_better": "neutral",
        "description": "Mean length of the input (prompt) in tokens. Defines the workload context size; longer prompts cost more in prefill.",
    },
    "output_sequence_length": {
        "unit": "tokens",
        "category": "tokens",
        "higher_is_better": "neutral",
        "description": "Mean length of the output (response) in tokens. Longer outputs cost more in decode and raise latency.",
    },
    "output_token_count": {
        "unit": "tokens",
        "category": "tokens",
        "higher_is_better": "neutral",
        "description": "Mean number of output tokens produced per request. Same as output_sequence_length in most cases.",
    },
    "reasoning_token_count": {
        "unit": "tokens",
        "category": "tokens",
        "higher_is_better": "neutral",
        "description": "Mean number of 'thinking'/reasoning tokens generated before the visible answer. Large for chain-of-thought workloads and inflates decode cost.",
    },
    "benchmark_duration": {
        "unit": "sec",
        "category": "misc",
        "higher_is_better": "neutral",
        "description": "Wall-clock duration of the whole benchmark run at this concurrency level. Mostly a sanity-check for run length, not a quality metric.",
    },
    "nvidia_average_gpu_power": {
        "unit": "W",
        "category": "gpu",
        "higher_is_better": "neutral",
        "description": "Mean power drawn by the GPU (watts) during the run. Higher power usually means the GPU is working harder; use it together with efficiency metrics.",
    },
    "nvidia_total_gpu_power": {
        "unit": "W",
        "category": "gpu",
        "higher_is_better": "neutral",
        "description": "Aggregate (summed) GPU power across all GPUs in the run. Useful when multiple GPUs are used.",
    },
    "nvidia_total_gpu_energy": {
        "unit": "J",
        "category": "gpu",
        "higher_is_better": "no",
        "description": "Total energy consumed by the GPU over the whole run (joules). Lower is more efficient for the same throughput.",
    },
    "nvidia_output_tokens_per_joule": {
        "unit": "tokens/J",
        "category": "efficiency",
        "higher_is_better": "yes",
        "description": "Output tokens produced per joule of energy. The core energy-efficiency metric: higher means more useful work per unit of energy.",
    },
    "nvidia_energy_per_output_token": {
        "unit": "mJ/token",
        "category": "efficiency",
        "higher_is_better": "no",
        "description": "Energy spent to generate one output token (millijoules). Lower is more efficient; the inverse of tokens-per-joule.",
    },
    "nvidia_energy_per_total_token": {
        "unit": "mJ/token",
        "category": "efficiency",
        "higher_is_better": "no",
        "description": "Energy spent per total (input + output) token. Lower is more efficient across the full token budget.",
    },
    "nvidia_energy_per_request": {
        "unit": "joules/request",
        "category": "efficiency",
        "higher_is_better": "no",
        "description": "Energy consumed to serve one complete request (joules). Lower is more efficient per request.",
    },
    "nvidia_energy_per_user": {
        "unit": "joules/user",
        "category": "efficiency",
        "higher_is_better": "no",
        "description": "Energy consumed per user over the run (joules). Lower is more efficient per user.",
    },
    "nvidia_output_tps_per_watt": {
        "unit": "tokens/sec/W",
        "category": "efficiency",
        "higher_is_better": "yes",
        "description": "Output tokens-per-second per watt of power. A performance-per-watt efficiency metric; higher is better.",
    },
    "nvidia_performance_per_watt": {
        "unit": "requests/sec/W",
        "category": "efficiency",
        "higher_is_better": "yes",
        "description": "Requests-per-second per watt of power. Throughput-per-watt efficiency; higher is better.",
    },
    "nvidia_energy_delay_product": {
        "unit": "J*s",
        "category": "efficiency",
        "higher_is_better": "no",
        "description": "Energy-delay product: energy consumed multiplied by latency. A combined efficiency/latency figure; lower is better (used in Pareto analysis).",
    },
    "http_req_duration": {
        "unit": "ms",
        "category": "http",
        "higher_is_better": "no",
        "description": "Total HTTP request duration (client view): from connection to full response. Includes network/connection overhead on top of server latency.",
    },
    "osl_mismatch_diff_pct": {
        "unit": "%",
        "category": "misc",
        "higher_is_better": "neutral",
        "description": "Percentage mismatch between the observed and expected output sequence length. Non-zero can indicate truncated or truncated-by-config responses.",
    },
    "osl_mismatch_count": {
        "unit": "requests",
        "category": "misc",
        "higher_is_better": "no",
        "description": "Number of requests whose output length did not match the expected value. Zero is ideal; non-zero flags truncated/over-long responses.",
    },
}


def _humanize(name: str) -> str:
    replacements = {
        "isl": "input sequence length",
        "osl": "output sequence length",
        "tps": "tokens/sec",
    }
    label = name
    for token, text in replacements.items():
        label = label.replace(token, text)
    return label.replace("_", " ").title().replace(" Isl", "ISL").replace(" Osl", "OSL")


def _guess_category(name: str) -> str:
    n = name.lower()
    if n.startswith("http"):
        return "http"
    if "throughput" in n or "tps" in n or "tokens_per" in n:
        return "throughput"
    if (
        "latency" in n
        or n.startswith("time_to")
        or "duration" in n
        or "waiting" in n
        or "credit_to" in n
    ):
        return "latency"
    if (
        "gpu" in n
        or "power" in n
        or "energy" in n
        or "watt" in n
        or "joule" in n
        or "energy_delay" in n
    ):
        return "gpu"
    if (
        "token" in n
        or "sequence" in n
        or "reasoning" in n
        or "in_flight" in n
        or n.endswith("_count")
    ):
        return "tokens"
    if "isl" in n or "osl" in n:
        return "tokens"
    return "misc"


def _auto_description(name: str, unit: str | None, category: str) -> str:
    label = _humanize(name)
    if unit:
        base = f"Value of {label} in {unit}, averaged across the run at each concurrency level."
    else:
        base = f"Value of {label}, averaged across the run at each concurrency level."
    return base


def get_metric_info(name: str, unit: str | None = None) -> dict[str, str]:
    if name in METRIC_INFO:
        info = dict(METRIC_INFO[name])
        info.setdefault("label", _humanize(name))
        if not info.get("unit") and unit:
            info["unit"] = unit
        return info
    category = _guess_category(name)
    return {
        "label": _humanize(name),
        "unit": unit or "",
        "category": category,
        "higher_is_better": "neutral",
        "description": _auto_description(name, unit, category),
    }


def _label_for(name: str, unit: str | None) -> str:
    info = METRIC_INFO.get(name)
    if info and "unit" in info:
        unit = info["unit"]
    unit = unit or ""
    return f"{_humanize(name)} [{unit}]" if unit else _humanize(name)


def build_dropdown_options(
    all_metrics: list[str], units: dict[str, str]
) -> list[dict[str, str]]:
    options: list[dict[str, str]] = []
    curated = sorted(
        METRIC_INFO,
        key=lambda m: (CATEGORY_ORDER.index(METRIC_INFO[m]["category"]), m),
    )
    seen: set[str] = set()
    for metric in curated:
        if metric in all_metrics:
            options.append(
                {"label": _label_for(metric, units.get(metric)), "value": metric}
            )
            seen.add(metric)
    extras = sorted(m for m in all_metrics if m not in seen)
    options.append({"label": "— other metrics —", "value": ""})
    for metric in extras:
        options.append(
            {"label": _label_for(metric, units.get(metric)), "value": metric}
        )
    return options

"""Interactive Dash visualizer for AIPerf sweep-aggregate artifacts.

Compares a chosen metric across benchmark types and concurrency, with the
ability to also compare across models, overlay two metrics, shade a min-max
uncertainty band and switch the y-axis to a log scale. Every model, supplier
and benchmark type is discovered automatically from the artifacts tree, so
new models show up without changing any code.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
import plotly.colors as pc
import plotly.graph_objects as go
import pandas as pd
from dash import Input, Output, State, dcc, html

sys.path.insert(0, str(Path(__file__).resolve().parent))
from data_loader import load_sweep_data  # noqa: E402
from metric_catalog import build_dropdown_options, get_metric_info  # noqa: E402


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Visualize AIPerf sweep aggregates")
    parser.add_argument(
        "--artifacts", default="artifacts", help="path to the artifacts directory"
    )
    parser.add_argument("--port", type=int, default=8050, help="port to serve on")
    parser.add_argument("--host", default="127.0.0.1", help="host to bind to")
    return parser.parse_args()


ARGS = _parse_args()
INDEX, DATA = load_sweep_data(ARGS.artifacts)

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True,
)

PALETTE = list(pc.qualitative.Pastel) + list(pc.qualitative.Bold)
X_TITLE = "Concurrency"


def _first_present(name: str) -> str:
    if name in INDEX["metrics"]:
        return name
    return INDEX["metrics"][0] if INDEX["metrics"] else ""


DEFAULT_METRIC = _first_present("request_throughput")
DEFAULT_METRIC2 = _first_present("request_latency")
metric_options = build_dropdown_options(INDEX["metrics"], INDEX["metric_units"])


def _filter(data: pd.DataFrame, models, benchmarks) -> pd.DataFrame:
    d = data
    if models:
        d = d[d["model"].isin(models)]
    if benchmarks:
        d = d[d["benchmarkType"].isin(benchmarks)]
    return d


def _label_unit(name: str) -> tuple[str, str]:
    info = get_metric_info(name, INDEX["metric_units"].get(name))
    return info["label"], info["unit"]


def _add_line(
    fig: go.Figure,
    x: pd.Series,
    y: pd.Series,
    name: str,
    color: str,
    yaxis: str = "y",
    log: bool = False,
) -> None:
    yv = y.astype(float)
    if log:
        yv = yv.clip(lower=1e-9)
    fig.add_trace(
        go.Scatter(
            x=list(x),
            y=list(yv),
            mode="lines+markers",
            name=name,
            line=dict(color=color, width=2.5),
            marker=dict(size=6),
            yaxis=yaxis,
        )
    )


def _add_band(
    fig: go.Figure,
    x: pd.Series,
    low: pd.Series,
    high: pd.Series,
    color: str,
    yaxis: str = "y",
    log: bool = False,
) -> None:
    low = low.fillna(high)
    high = high.fillna(low)
    if log:
        low = low.clip(lower=1e-9)
        high = high.clip(lower=1e-9)
    if (low == high).all() or low.isna().all():
        return
    fig.add_trace(
        go.Scatter(
            x=list(x) + list(x[::-1]),
            y=list(low) + list(high[::-1]),
            fill="toself",
            fillcolor=color,
            line=dict(width=0),
            opacity=0.14,
            hoverinfo="skip",
            showlegend=False,
            yaxis=yaxis,
        )
    )


def build_figure(
    metric: str, metric2: str, models, benchmarks, layout: str, band: bool, log: bool
) -> go.Figure:
    d = _filter(DATA, models, benchmarks)
    fig = go.Figure()

    if layout == "overlay":
        _build_overlay(fig, d, metric, metric2, band, log)
    else:
        _build_single_metric(fig, d, metric, layout, band, log)

    y_type = "log" if log else "linear"
    layout_ = dict(
        title=f"{_label_unit(metric)[0]} vs {X_TITLE}",
        xaxis=dict(title=X_TITLE),
        yaxis=dict(
            title=f"{_label_unit(metric)[0]} ({_label_unit(metric)[1]})"
            if _label_unit(metric)[1]
            else _label_unit(metric)[0],
            type=y_type,
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
        plot_bgcolor="white",
        margin=dict(l=10, r=10, t=60, b=10),
    )
    if layout == "overlay":
        layout_["yaxis2"] = dict(
            title=f"{_label_unit(metric2)[0]} ({_label_unit(metric2)[1]})"
            if _label_unit(metric2)[1]
            else _label_unit(metric2)[0],
            type=y_type,
            overlaying="y",
            side="right",
        )
    fig.update_layout(**layout_)
    return fig


def _build_single_metric(
    fig: go.Figure, d: pd.DataFrame, metric: str, layout: str, band: bool, log: bool
) -> None:
    dm = d[d["metric"] == metric]
    if layout == "combo":
        groups = dm.groupby(["model", "benchmarkType"])
        for i, ((model, bt), g) in enumerate(groups):
            g = g.sort_values("concurrency")
            color = PALETTE[i % len(PALETTE)]
            if band:
                _add_band(fig, g["concurrency"], g["min"], g["max"], color, log=log)
            _add_line(
                fig, g["concurrency"], g["mean"], f"{model} · {bt}", color, log=log
            )
    else:
        for i, (bt, g) in enumerate(dm.groupby("benchmarkType")):
            g = g.sort_values("concurrency")
            color = PALETTE[i % len(PALETTE)]
            if band:
                _add_band(fig, g["concurrency"], g["min"], g["max"], color, log=log)
            _add_line(fig, g["concurrency"], g["mean"], bt, color, log=log)


def _build_overlay(
    fig: go.Figure, d: pd.DataFrame, metric: str, metric2: str, band: bool, log: bool
) -> None:
    dm1 = d[d["metric"] == metric]
    dm2 = d[d["metric"] == metric2]
    for i, (bt, g) in enumerate(dm1.groupby("benchmarkType")):
        g = g.sort_values("concurrency")
        color = PALETTE[i % len(PALETTE)]
        if band:
            _add_band(fig, g["concurrency"], g["min"], g["max"], color, log=log)
        _add_line(
            fig,
            g["concurrency"],
            g["mean"],
            f"{_label_unit(metric)[0]} · {bt}",
            color,
            log=log,
        )
    for i, (bt, g) in enumerate(dm2.groupby("benchmarkType")):
        g = g.sort_values("concurrency")
        color = PALETTE[i % len(PALETTE)]
        _add_line(
            fig,
            g["concurrency"],
            g["mean"],
            f"{_label_unit(metric2)[0]} · {bt}",
            color,
            yaxis="y2",
            log=log,
        )
        fig.data[-1]["line"]["dash"] = "dash"


def _arrow(hib: str) -> str:
    return {
        "yes": "↑ higher is better",
        "no": "↓ lower is better",
        "neutral": "— neutral",
    }.get(hib, "")


def _metric_card(name: str) -> html.Div:
    info = get_metric_info(name, INDEX["metric_units"].get(name))
    unit = info.get("unit", "")
    return html.Div(
        [
            html.Div(
                [
                    html.Div(f"{info['label']}", className="fw-bold fs-5"),
                    html.Span(
                        f" [{unit}]", className="text-muted ms-2" if unit else "ms-2"
                    )
                    if unit
                    else html.Span(),
                    html.Span(
                        f" · {info.get('category', '')}", className="text-muted ms-2"
                    ),
                ]
            ),
            html.Div(
                _arrow(info.get("higher_is_better", "neutral")),
                className="text-muted mt-1",
            ),
            html.Div(info.get("description", ""), className="mt-2"),
        ],
        className="mb-3",
    )


@app.callback(
    Output("description", "children"),
    [Input("metric", "value"), Input("metric2", "value"), Input("layout", "value")],
)
def render_description(metric, metric2, layout):
    cards = [html.Div(_metric_card(metric))] if metric else []
    if layout == "overlay" and metric2:
        cards.append(
            html.Div(
                [
                    html.Div(
                        "Second metric (right axis)",
                        className="fw-bold mb-1 text-muted",
                    ),
                    _metric_card(metric2),
                ]
            )
        )
    return cards


@app.callback(
    Output("plot", "figure"),
    [
        Input("metric", "value"),
        Input("metric2", "value"),
        Input("models", "value"),
        Input("benchmarks", "value"),
        Input("layout", "value"),
        Input("band", "value"),
        Input("log", "value"),
    ],
)
def update_plot(metric, metric2, models, benchmarks, layout, band, log):
    if not metric:
        return go.Figure().update_layout(title="No variable selected")
    return build_figure(
        metric, metric2 or metric, models, benchmarks, layout, band, log
    )


@app.callback(
    Output("table", "children"),
    [Input("metric", "value"), Input("models", "value"), Input("benchmarks", "value")],
)
def render_table(metric, models, benchmarks):
    if not metric:
        return html.Div("Select a variable to see the underlying numbers.")
    d = _filter(DATA, models, benchmarks)
    d = d[d["metric"] == metric][
        ["concurrency", "benchmarkType", "model", "mean", "min", "max", "unit"]
    ]
    d = d.sort_values(["benchmarkType", "model", "concurrency"])
    if d.empty:
        return html.Div("No data for the current selection.")
    info = get_metric_info(metric, INDEX["metric_units"].get(metric))
    head = (
        f"{info['label']} [{info.get('unit', '')}] by benchmark, model and concurrency"
    )
    rows = [html.Tr([html.Td(x) for x in d.columns])]
    for _, r in d.iterrows():
        cells = []
        for c in d.columns:
            v = r[c]
            text = (
                f"{v:,.4f}".rstrip("0").rstrip(".")
                if isinstance(v, float) and not pd.isna(v)
                else v
            )
            cells.append(html.Td(text))
        rows.append(html.Tr(cells))
    return html.Div(
        [
            html.Div(head, className="fw-bold mb-2"),
            html.Table(
                [rows],
                className="table table-sm table-hover",
                style={"font-size": "0.85rem"},
            ),
        ]
    )


def _control(col, children) -> dbc.Col:
    return dbc.Col(children, className="mb-3", lg=col, md=6, sm=12)


app.layout = dbc.Container(
    [
        dbc.Row(
            [
                html.H1(
                    "AIPerf sweep aggregate explorer", className="text-center my-3"
                ),
            ],
            className="justify-content-center",
        ),
        dbc.Alert(
            [
                "No sweep-aggregate data found. Run a benchmark first, or point "
                "--artifacts at a directory containing artifacts/{supplier}/{model}/"
                "{benchmarkType}/sweep_aggregate/.",
            ],
            color="warning",
            className="my-3",
        )
        if not INDEX["metrics"]
        else html.Div(),
        dbc.Row(
            [
                _control(
                    3,
                    [
                        html.Label("Variable (Y axis)", className="fw-bold"),
                        dcc.Dropdown(
                            id="metric",
                            options=metric_options,
                            value=DEFAULT_METRIC,
                            searchable=True,
                            clearable=False,
                            placeholder="choose a variable",
                        ),
                    ],
                ),
                _control(
                    3,
                    [
                        html.Label(
                            "Variable 2 (overlay, right axis)", className="fw-bold"
                        ),
                        dcc.Dropdown(
                            id="metric2",
                            options=metric_options,
                            value=DEFAULT_METRIC2,
                            searchable=True,
                            clearable=False,
                            placeholder="second variable",
                        ),
                    ],
                ),
                _control(
                    3,
                    [
                        html.Label("Layout", className="fw-bold"),
                        dcc.RadioItems(
                            id="layout",
                            options=[
                                {
                                    "label": "  one line per benchmark type",
                                    "value": "benchmarkType",
                                },
                                {
                                    "label": "  one line per model × benchmark",
                                    "value": "combo",
                                },
                                {"label": "  two-metric overlay", "value": "overlay"},
                            ],
                            value="benchmarkType",
                            inline=True,
                        ),
                    ],
                ),
                _control(
                    3,
                    [
                        html.Label("Options", className="fw-bold"),
                        dbc.Switch(id="band", label="min–max band", value=True),
                        dbc.Switch(id="log", label="log y-axis", value=False),
                    ],
                ),
                _control(
                    3,
                    [
                        html.Label(
                            f"Models ({len(INDEX['models'])})", className="fw-bold"
                        ),
                        dcc.Dropdown(
                            id="models",
                            options=[{"label": m, "value": m} for m in INDEX["models"]],
                            value=INDEX["models"],
                            multi=True,
                            clearable=False,
                        ),
                    ],
                ),
                _control(
                    3,
                    [
                        html.Label(
                            f"Benchmark types ({len(INDEX['benchmarkTypes'])})",
                            className="fw-bold",
                        ),
                        dcc.Dropdown(
                            id="benchmarks",
                            options=[
                                {"label": b, "value": b}
                                for b in INDEX["benchmarkTypes"]
                            ],
                            value=INDEX["benchmarkTypes"],
                            multi=True,
                            clearable=False,
                        ),
                    ],
                ),
            ]
        ),
        dbc.Row(
            [
                _control(8, [dcc.Graph(id="plot", style={"height": "70vh"})]),
                _control(
                    4,
                    [
                        html.Div("Explanations", className="fw-bold mb-2"),
                        html.Div(id="description"),
                    ],
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("Underlying numbers", className="fw-bold mb-2"),
                        html.Div(id="table"),
                    ]
                )
            ]
        ),
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run(debug=True, host=ARGS.host, port=ARGS.port)

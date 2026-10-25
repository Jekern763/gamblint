import ast
import sys
from pathlib import Path

import camel_converter
import pandas as pd
import plotly.graph_objects as go

CODE_DIR = Path(__file__).resolve().parents[1]
FIGURE_GENERATORS_DIR = Path(__file__).resolve().parent
METRIC_GENERATORS_DIR = CODE_DIR / "metric_generators"

for import_path in (
    CODE_DIR,
    FIGURE_GENERATORS_DIR,
    METRIC_GENERATORS_DIR,
):
    path_string = str(import_path)
    if path_string not in sys.path:
        sys.path.append(path_string)

from algorithm_metrics import AlgorithmMetrics
from algorithm_paths import (
    PER_ALGORITHM_FIGURES_DIR,
    RAW_DATA_DIR,
)
from graph_config import (
    ALGORITHM_DFS,
    ALGORITHM_DFS_BY_GUESS,
    ALGORITHM_DFS_BY_PEEKS,
    ALGORITHMS,
    FONT_SIZE,
    HEIGHT,
    WIDTH,
)
from graph_utils import save_multi_line

# ========== GRAPHING GUESS FREQUENCY BY GUESS ========== #

fig = go.Figure()

for algorithm in ALGORITHMS:
    df = ALGORITHM_DFS[algorithm]

    distribution = ast.literal_eval(df.loc[0, "guess_frequency"])

    guesses = sorted(int(g) for g in distribution)
    frequencies = [
        distribution[str(g)] if str(g) in distribution else distribution[g]
        for g in guesses
    ]

    fig.add_trace(
        go.Scatter(
            x=guesses,
            y=frequencies,
            mode="lines+markers",
            name=(algorithm.replace("_agent", "").replace("_", " ").title()),
        )
    )

fig.update_layout(
    title="Guess Distribution by Algorithm",
    width=WIDTH,
    height=HEIGHT,
    template="simple_white",
    font={"size": FONT_SIZE},
    title_font_size=24,
    xaxis_title="Guess",
    yaxis_title="Guess Frequency",
    legend_title_text="Algorithm",
)

fig.update_xaxes(
    dtick=1,
    showgrid=True,
)

fig.update_yaxes(
    showgrid=True,
    rangemode="tozero",
)

output_path = PER_ALGORITHM_FIGURES_DIR / "guess_distribution_by_algorithm.png"
PER_ALGORITHM_FIGURES_DIR.mkdir(parents=True, exist_ok=True)
fig.write_image(str(output_path))


# ========== GRAPHING METRCIS BY Guess, Roll, Peeks =========#
condition_dfs = {
    "guess": ALGORITHM_DFS_BY_GUESS,
    "peek_average": ALGORITHM_DFS_BY_PEEKS,
}
graphs = [
    "average_payout",
    "exact_hit_rate",
    "mean_absolute_error",
    "average_operations",
]
for condition, dfs in condition_dfs.items():
    for y_value in graphs:
        title = f"{y_value.replace('_', ' ').title()} for {condition.title()}"
        save_multi_line(
            dfs,
            condition,
            y_value,
            title,
            condition.replace("_", " ").title(),
            y_value.replace("_", " ").title(),
            PER_ALGORITHM_FIGURES_DIR / f"{y_value}_for_{condition}.png",
        )
# ========== GRAPHING METRIC VS METRIC ie PEEK VARIANCE VS AVERAGE PAYOUT
# going to use algorithm metrics to pull the metrics that I didn't automatically generate
graphs = [
    "average_payout",
    "exact_hit_rate",
    "mean_absolute_error",
    "average_operations",
    "average_deviation_guess",
]
metrics_to_compare = ["peek_variance", "roll", "total_operations", "payout"]
metrics_dfs = {
    # metric: [dfs]
}

for i in metrics_to_compare:
    metrics_dfs[i] = {}

for algorithm in ALGORITHMS:
    path = RAW_DATA_DIR / f"{algorithm}_10000.parquet"
    algorithm_metrics = AlgorithmMetrics(path)
    for metric_x in metrics_to_compare:
        metric_x_df = pd.DataFrame(
            algorithm_metrics.filtered(metric_x, algorithm_metrics.all)
        )
        metrics_dfs[metric_x][algorithm] = metric_x_df

for metric_x in metrics_to_compare:
    for metric_y in graphs:  # bad naming convention, but take what you can get
        if (
            metric_y != metric_x
            and not (metric_x == "payout" and metric_y == "average_payout")
            and not (
                metric_x == "total_operations" and metric_y == "average_operations"
            )
        ):
            title = f"{metric_y.replace('_', ' ').title()} for {metric_x.replace('_', ' ').title()}"
            save_multi_line(
                metrics_dfs[metric_x],
                metric_x,
                metric_y,
                title,
                metric_x,
                metric_y,
                PER_ALGORITHM_FIGURES_DIR
                / (camel_converter.to_snake(f"{metric_y}_for_{metric_x}") + ".png"),
            )

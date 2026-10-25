# graphs for baseline constant algorithms, 2-12
import sys
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
FIGURE_GENERATORS_DIR = Path(__file__).resolve().parent

for import_path in (CODE_DIR, FIGURE_GENERATORS_DIR):
    path_string = str(import_path)
    if path_string not in sys.path:
        sys.path.append(path_string)

import camel_converter
import pandas as pd
from algorithm_paths import BASELINE_FIGURES_DIR, METRIC_TABLE_DIR
from graph_config import CONSTANT_ALGORITHMS
from graph_utils import save_line, save_multi_line

GRAPHS = [
    (
        "average_payout",
        "Average Payout for Constant Guess",
        "Average Payout",
    ),
    (
        "exact_hit_rate",
        "Exact Hit Rate for Constant Guess",
        "Exact Hit Rate",
    ),
    (
        "mean_absolute_error",
        "Mean Absolute Error for Constant Guess",
        "Mean Absolute Error",
    ),
    ("maximum_payout", "Maximum Payout for Constant Guess", "Maximum Payout"),
    ("median_payout", "Median Payout for Constant Guess", "Median Payout"),
]

rows = []

for algorithm in CONSTANT_ALGORITHMS:
    df = pd.read_csv(METRIC_TABLE_DIR / algorithm / f"{algorithm}.csv")

    rows.append(
        {
            "constant": int(algorithm.replace("constant_agent_", "")),
            **{metric: df.loc[0, metric] for metric, _, _ in GRAPHS},
        }
    )

constant_df = pd.DataFrame(rows).sort_values("constant")

for metric, title, ylabel in GRAPHS:
    save_line(
        constant_df,
        x="constant",
        y=metric,
        output_path=BASELINE_FIGURES_DIR / f"baseline_{metric}.png",
        title=title,
        x_label="Constant Guess",
        y_label=ylabel,
    )

# ========== GRAPHING BASIC METRICS BY ROLL, PEEKS ==========
CONSTANT_ALGORITHM_DFS_BY_ROLL = {
    algorithm: pd.read_csv(METRIC_TABLE_DIR / algorithm / f"{algorithm}_by_roll.csv")
    for algorithm in CONSTANT_ALGORITHMS
}

CONSTANT_ALGORITHM_DFS_BY_PEEKS = {
    algorithm: pd.read_csv(METRIC_TABLE_DIR / algorithm / f"{algorithm}_by_peeks.csv")
    for algorithm in CONSTANT_ALGORITHMS
}
condition_dfs = {
    "peek_average": CONSTANT_ALGORITHM_DFS_BY_PEEKS,
}
for condition, dfs in condition_dfs.items():
    graphs = [
        # y_values, graph title)
        "average_payout",
        "exact_hit_rate",
        "mean_absolute_error",
    ]

    for y_value in graphs:
        title = f"{y_value.replace('_', ' ').title()} per {condition.title()}"
        save_multi_line(
            dfs,
            condition,
            y_value,
            title,
            condition.replace("_", " ").title(),
            y_value.replace("_", " ").title(),
            BASELINE_FIGURES_DIR / f"baseline_{camel_converter.to_snake(title)}.png",
        )

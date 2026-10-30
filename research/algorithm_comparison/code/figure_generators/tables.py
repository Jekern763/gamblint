import sys
from ast import literal_eval
from pathlib import Path

import dataframe_image as dfi
import pandas as pd

CODE_DIR = Path(__file__).resolve().parents[1]
FIGURE_GENERATORS_DIR = Path(__file__).resolve().parent

for import_path in (CODE_DIR, FIGURE_GENERATORS_DIR):
    path_string = str(import_path)
    if path_string not in sys.path:
        sys.path.append(path_string)

from algorithm_paths import TABLES_FIGURES_DIR
from graph_config import ALGORITHM_DFS


def save_path(file_type: str, name: str) -> Path:
    TABLES_FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    return TABLES_FIGURES_DIR / f"{name}.{file_type}"


def pretty_df(df):
    return df.columns.str.replace("_", " ").str.title()


"""
Tables to make:
- summary: basic stats per algorithm
- effeciency
- guess behavior
"""

# 1: Summary Table

summary = pd.concat(ALGORITHM_DFS, names=["Algorithm"]).reset_index(level=0)
summary = summary[
    [
        "Algorithm",
        "average_payout",
        "mean_absolute_error",
        "mean_squared_error",
        "exact_hit_rate",
    ]
]
summary.columns = pretty_df(summary)
summary = summary.sort_values(by="Average Payout", ascending=False)
dfi.export(summary, str(save_path("png", "summary_table")))
summary.to_markdown(str(save_path("md", "summary_table")), index=False)

# 2: Effeciency Table

effeciency = pd.concat(ALGORITHM_DFS, names=["Algorithm"]).reset_index(level=0)

effeciency["Operations Per Payout"] = (
    effeciency["average_operations"] / effeciency["average_payout"]
)

effeciency = effeciency[
    [
        "Algorithm",
        "Operations Per Payout",
        "average_operations",
        "maximum_operations",
        "average_payout",
    ]
]

effeciency.columns = pretty_df(effeciency)
effeciency = effeciency.sort_values(by="Average Operations", ascending=True)
dfi.export(effeciency, str(save_path("png", "effeciency_table")))
effeciency.to_markdown(str(save_path("md", "effeciency_table")), index=False)

# 3: Guess Behavior

guess_behavior = pd.concat(ALGORITHM_DFS, names=["Algorithm"]).reset_index(level=0)

guess_behavior["Most Guessed"] = guess_behavior["guess_frequency"].apply(
    lambda d: max(literal_eval(d), key=literal_eval(d).get)
)

guess_behavior["Average Guess"] = guess_behavior["guess_frequency"].apply(
    lambda d: (
        sum(float(k) * float(w) for k, w in literal_eval(d).items())
        / sum(float(w) for w in literal_eval(d).values())
    )
)

guess_behavior = guess_behavior[
    [
        "Algorithm",
        "Average Guess",
        "Most Guessed",
        "average_deviation_guess",
        "mean_absolute_error",
        "exact_hit_rate",
    ]
]

guess_behavior.columns = pretty_df(guess_behavior)
dfi.export(guess_behavior, str(save_path("png", "guess_behavior_table")))
guess_behavior.to_markdown(str(save_path("md", "guess_behavior_table")))

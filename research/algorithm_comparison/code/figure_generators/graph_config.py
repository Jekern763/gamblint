import sys
from pathlib import Path

import pandas as pd

# Make algorithm_paths.py importable from this nested directory.
CODE_DIR = Path(__file__).resolve().parents[1]
if str(CODE_DIR) not in sys.path:
    sys.path.append(str(CODE_DIR))

from algorithm_paths import FIGURES_DIR, METRIC_TABLE_DIR

ALGORITHMS = [
    "random_agent",
    "reflection_agent",
    "invariant_agent",
    "gamblers_fallacy_agent",
    "single_path_agent",
    "expectimax_agent",
    "average_agent",
]

CONSTANT_ALGORITHMS = [f"constant_agent_{i}" for i in range(2, 13)]


def read_metric_table(algorithm: str, suffix: str = "") -> pd.DataFrame:
    path = METRIC_TABLE_DIR / algorithm / f"{algorithm}{suffix}.csv"
    return pd.read_csv(path)


ALGORITHM_DFS = {algorithm: read_metric_table(algorithm) for algorithm in ALGORITHMS}

ALGORITHM_DFS_BY_GUESS = {
    algorithm: read_metric_table(algorithm, "_by_guess") for algorithm in ALGORITHMS
}

ALGORITHM_DFS_BY_ROLL = {
    algorithm: read_metric_table(algorithm, "_by_roll") for algorithm in ALGORITHMS
}

ALGORITHM_DFS_BY_PEEKS = {
    algorithm: read_metric_table(algorithm, "_by_peeks") for algorithm in ALGORITHMS
}

# Shared plotting dimensions.
WIDTH = 900
HEIGHT = 600
FONT_SIZE = 18

# Figure output locations.
BASELINE_FIGURES_DIR = FIGURES_DIR / "baseline"
MISC_FIGURES_DIR = FIGURES_DIR / "misc"
OVERALL_FIGURES_DIR = FIGURES_DIR / "overall"
PER_ALGORITHM_FIGURES_DIR = FIGURES_DIR / "per_algorithm"
TABLES_FIGURES_DIR = FIGURES_DIR / "tables"

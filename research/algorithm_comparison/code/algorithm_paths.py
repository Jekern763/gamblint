import sys
from pathlib import Path

# algorithm_paths.py lives in algorithm_comparison/code/
RESEARCH_ROOT = Path(__file__).resolve().parents[2]
REPOSITORY_ROOT = RESEARCH_ROOT.parent

ALGORITHM_DIR = RESEARCH_ROOT / "algorithm_comparison"
CODE_DIR = ALGORITHM_DIR / "code"
METRIC_GENERATORS_DIR = CODE_DIR / "metric_generators"
FIGURE_GENERATORS_DIR = CODE_DIR / "figure_generators"

DATA_DIR = ALGORITHM_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
METRIC_TABLE_DIR = DATA_DIR / "metric_tables"

FIGURES_DIR = ALGORITHM_DIR / "figures"
BASELINE_FIGURES_DIR = FIGURES_DIR / "baseline"
MISC_FIGURES_DIR = FIGURES_DIR / "misc"
OVERALL_FIGURES_DIR = FIGURES_DIR / "overall"
PER_ALGORITHM_FIGURES_DIR = FIGURES_DIR / "per_algorithm"
TABLES_FIGURES_DIR = FIGURES_DIR / "tables"

BACKEND_ROOT = REPOSITORY_ROOT / "backend"


def append_to_sys_path(path: str | Path) -> None:
    """Append a path to sys.path if it is not already present."""
    path_string = str(path)
    if path_string not in sys.path:
        sys.path.append(path_string)


def ensure_backend_importable() -> None:
    """Make the original backend packages importable."""
    if not BACKEND_ROOT.is_dir():
        raise FileNotFoundError(f"Backend directory was not found: {BACKEND_ROOT}")

    append_to_sys_path(BACKEND_ROOT)

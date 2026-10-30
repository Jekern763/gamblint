import sys
from pathlib import Path

import pandas as pd

RESEARCH_ROOT = Path(__file__).resolve().parents[3]
SHARED_CODE_DIR = RESEARCH_ROOT / "shared" / "code"
GAME_ANALYSIS_DIR = RESEARCH_ROOT / "game_analysis"
GAME_DATA_DIR = GAME_ANALYSIS_DIR / "data"

if str(SHARED_CODE_DIR) not in sys.path:
    sys.path.insert(0, str(SHARED_CODE_DIR))


RESEARCH_ROOT = Path(__file__).resolve().parents[3]
SHARED_CODE_DIR = RESEARCH_ROOT / "shared" / "code"
GAME_ANALYSIS_DIR = RESEARCH_ROOT / "game_analysis"
GAME_DATA_DIR = GAME_ANALYSIS_DIR / "data"


def get_dataframes() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return the per-history and per-configuration datasets."""
    analysis_by_history = pd.read_pickle(GAME_DATA_DIR / "analysis_by_history.pkl")
    analysis_by_config = pd.read_pickle(GAME_DATA_DIR / "analysis_by_dice_config.pkl")
    return analysis_by_history, analysis_by_config

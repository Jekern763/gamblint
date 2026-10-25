import csv
import sys
from pathlib import Path

# Make code/ and metric_generators/ importable.
CODE_DIR = Path(__file__).resolve().parents[1]
METRIC_GENERATORS_DIR = Path(__file__).resolve().parent

for import_path in (CODE_DIR, METRIC_GENERATORS_DIR):
    path_string = str(import_path)
    if path_string not in sys.path:
        sys.path.append(path_string)

from algorithm_metrics import AlgorithmMetrics
from algorithm_paths import METRIC_TABLE_DIR, RAW_DATA_DIR


def write_csv(path: str | Path, data: list | dict) -> None:
    if isinstance(data, dict):
        data = [data]

    if not data:
        return

    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    all_keys = []
    for item in data:
        for key in item:
            if key not in all_keys:
                all_keys.append(key)

    with file_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=all_keys)
        writer.writeheader()
        writer.writerows(data)


def main() -> None:
    raw_files = sorted(RAW_DATA_DIR.glob("*_10000.parquet"))

    if not raw_files:
        raise FileNotFoundError(
            f"No benchmark Parquet files found in {RAW_DATA_DIR}. "
            "Run benchmark_algorithms.py first."
        )

    for raw_data_path in raw_files:
        algorithm_name = raw_data_path.stem.removesuffix("_10000")
        algorithm_metrics = AlgorithmMetrics(raw_data_path)

        algorithm_output_dir = METRIC_TABLE_DIR / algorithm_name

        # Overall metrics.
        write_csv(
            algorithm_output_dir / f"{algorithm_name}.csv",
            algorithm_metrics.all(),
        )

        # Metrics grouped by actual roll.
        write_csv(
            algorithm_output_dir / f"{algorithm_name}_by_roll.csv",
            algorithm_metrics.filtered("roll", algorithm_metrics.all),
        )

        # Metrics grouped by guess.
        write_csv(
            algorithm_output_dir / f"{algorithm_name}_by_guess.csv",
            algorithm_metrics.filtered("guess", algorithm_metrics.all),
        )

        # Metrics grouped by average peek.
        write_csv(
            algorithm_output_dir / f"{algorithm_name}_by_peeks.csv",
            algorithm_metrics.filtered("peek_average", algorithm_metrics.all),
        )


if __name__ == "__main__":
    main()

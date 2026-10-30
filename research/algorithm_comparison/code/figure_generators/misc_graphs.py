import sys
from pathlib import Path

import plotly.express as px

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
from algorithm_paths import MISC_FIGURES_DIR, RAW_DATA_DIR
from graph_config import ALGORITHMS


def save_heatmap(
    df,
    x,
    y,
    z,
    title,
    x_label,
    y_label,
    color_label,
    filename,
):
    pivot = df.pivot(
        index=y,
        columns=x,
        values=z,
    )

    fig = px.imshow(
        pivot,
        text_auto=".3f",
        color_continuous_scale="Viridis",
        labels={
            "x": x_label,
            "y": y_label,
            "color": color_label,
        },
        title=title,
        aspect="equal",
    )

    fig.update_xaxes(dtick=1)
    fig.update_yaxes(dtick=1)

    MISC_FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    output_path = MISC_FIGURES_DIR / f"{filename}.png"
    fig.write_image(str(output_path), scale=11)


def main() -> None:
    for algorithm in ALGORITHMS:
        raw_path = RAW_DATA_DIR / f"{algorithm}_10000.parquet"
        metrics = AlgorithmMetrics(raw_path)
        df = metrics.df

        heatmap_df = df.groupby(["roll", "guess"]).agg(
            frequency=("guess", "size"),
            average_payout=("payout", "mean"),
            average_operations=("total_operations", "mean"),
        )

        heatmap_df["frequency"] /= heatmap_df.groupby(level=0)["frequency"].transform(
            "sum"
        )
        heatmap_df = heatmap_df.reset_index()

        save_heatmap(
            heatmap_df,
            x="roll",
            y="guess",
            z="frequency",
            title=f"{algorithm} Guess Frequency",
            x_label="Actual Roll",
            y_label="Guess",
            color_label="Frequency",
            filename=f"{algorithm}_roll_guess_frequency",
        )

        save_heatmap(
            heatmap_df,
            x="roll",
            y="guess",
            z="average_operations",
            title=f"{algorithm} Average Operations",
            x_label="Actual Roll",
            y_label="Guess",
            color_label="Average Operations",
            filename=f"{algorithm}_roll_guess_average_operations",
        )


if __name__ == "__main__":
    main()

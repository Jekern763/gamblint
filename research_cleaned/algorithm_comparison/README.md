# Algorithm Comparison README

This section explores how well different algorithms play the game and how much computation they require. It compares seven non-constant algorithms against eleven constant-guess algorithms, which serve as baselines. The goal is to understand the strengths and weaknesses of the different approaches and identify interesting relationships between performance, guessing behavior, and computational effort.

## The Pipeline

The research follows a four-stage pipeline:

1. **Benchmarking:** The original algorithm implementations in `backend/agent_algorithms/` are imported and run through thousands of simulated games. The raw results are saved as Parquet files.
2. **Metric generation:** The raw results are processed into CSV tables containing overall performance metrics and metrics grouped by guess, actual roll, and average peek.
3. **Figure generation:** The metric tables and raw data are used to create graphs comparing the algorithms, examining their behavior, and visualizing their computational costs.
4. **Interpretation:** The generated graphs and tables provide a basis for comparing algorithms and identifying patterns worth further investigation.

The benchmark data can be regenerated independently of the figures. If only the plotting code changes, there is no need to rerun the simulations, provided the underlying data and metric definitions remain unchanged.

## Running the Pipeline

Run these commands from the root of the cleaned research directory, where `pyproject.toml` is located. The commands use `uv` to run the scripts in the project's Python environment.

### 1. Generate benchmark data

```bash
uv run python algorithm_comparison/code/benchmark_algorithms.py
```

This benchmarks all 18 agents, currently using 10,000 rounds per agent, and writes the raw results to `algorithm_comparison/data/raw/`.

### 2. Generate metric tables

```bash
uv run python algorithm_comparison/code/metric_generators/metrics_generator.py
```

This processes the raw Parquet files and generates four CSV tables per agent in `algorithm_comparison/data/metric_tables/`.

### 3. Generate figures and tables

Run the five figure generators:

```bash
uv run python algorithm_comparison/code/figure_generators/baseline_graphs.py
uv run python algorithm_comparison/code/figure_generators/misc_graphs.py
uv run python algorithm_comparison/code/figure_generators/overall_graphs.py
uv run python algorithm_comparison/code/figure_generators/per_algorithm.py
uv run python algorithm_comparison/code/figure_generators/tables.py
```

These save the generated figures and summary tables under `algorithm_comparison/figures/`.

**Important:** The figure generators expect the metric tables to exist already. If you change the benchmark results or metric calculations, regenerate the metric tables before rebuilding the figures.

## code

### `algorithm_paths.py`

Centralizes the paths used throughout this section, including the data directories, figure destinations, and original backend location. It also provides a helper for making the backend importable.

### `benchmark_algorithms.py`

Constructs the seven non-constant agents and eleven constant-guess agents, then runs the benchmarks and saves their results.

### `benchmark_runner.py`

Runs an agent for a specified number of rounds, records the results and a function-call-based measure of computational effort, and optionally saves the results as a Parquet file.

### `metric_generators/algorithm_metrics.py`

Loads a raw benchmark dataset and calculates performance, accuracy, guessing behavior, and computational metrics. It also supports calculating metrics grouped by particular game conditions.

### `metric_generators/metrics_generator.py`

Processes the raw datasets for all agents and generates the four CSV metric tables for each one.

### `figure_generators/graph_config.py`

Loads the metric tables used by the figure generators and defines shared plotting settings.

### `figure_generators/graph_utils.py`

Contains reusable plotting functions to keep the generated figures consistent.

### `figure_generators/baseline_graphs.py`

Compares the constant-guess agents and shows how their performance changes depending on which number they always guess.

### `figure_generators/misc_graphs.py`

Generates heatmaps showing how often agents make particular guesses and how their computational effort varies with the actual roll and guess.

### `figure_generators/overall_graphs.py`

Compares the non-constant algorithms using overall performance and computational metrics. It also generates the Pareto-frontier plot.

### `figure_generators/per_algorithm.py`

Examines individual algorithm behavior in more detail, including how performance and other metrics vary with guesses, rolls, and peek statistics.

### `figure_generators/tables.py`

Generates summary, efficiency, and guess-behavior tables in Markdown and image formats.

## data

Contains the raw benchmark results and the metric tables derived from them.

### `raw/`

Contains one Parquet file per algorithm, currently generated from 10,000 simulated rounds per agent. These files record the game results, guesses, peeks, payouts, and computational measurements.

### `metric_tables/`

Contains the CSV tables generated from the raw results. Each agent has an overall metrics table and separate tables grouped by guess, actual roll, and average peek.

## figures

Contains the generated plots and summary tables, organized into five subdirectories.

### `baseline/`

Graphs comparing the constant-guess agents.

### `misc/`

Heatmaps examining guess frequencies and computational effort.

### `overall/`

Graphs comparing the non-constant algorithms, including the Pareto frontier.

### `per_algorithm/`

Graphs examining algorithm behavior under different conditions.

### `tables/`

Summary, efficiency, and guess-behavior tables, saved in Markdown and PNG formats.

## Backend Dependency

The actual algorithm implementations are maintained in `backend/agent_algorithms/`. The benchmark code imports those original implementations rather than maintaining separate copies in the research directory. This ensures that the research benchmarks the same algorithms used by the main project.

The benchmark scripts use `algorithm_paths.py` to make the backend importable and to centralize filesystem paths. The raw benchmark results are stored in Parquet, and the derived metrics are stored in CSV; neither format requires loading serialized agent instances.

## Notes on Interpretation

The computational-effort metric is based on function-call counts collected with Python's `cProfile`. It is useful for comparing the implementations under the same measurement setup, but it is not a literal count of CPU instructions or mathematical operations.

The generated metrics and figures are tools for exploration and comparison. Observed relationships can motivate further investigation, but they do not necessarily establish causation or explain why an algorithm behaves as it does.

import cProfile
import pstats
from pathlib import Path
from typing import Any

import pandas as pd
from algorithm_paths import RAW_DATA_DIR


def benchmark(
    agent: Any,
    run_name: str,
    num_runs: int,
    save_results: bool = True,
    output_dir: str | Path | None = None,
) -> list[dict]:
    results = []

    for i in range(num_runs):
        local_profiler = cProfile.Profile()
        local_profiler.enable()

        try:
            result = agent.simulate_round()
        finally:
            local_profiler.disable()

        local_stats = pstats.Stats(local_profiler)
        result["total_operations"] = local_stats.total_calls
        result["algorithm"] = run_name
        result["run_num"] = i
        results.append(result)

        agent.reset_session()

    if save_results:
        destination = Path(output_dir) if output_dir else RAW_DATA_DIR
        destination.mkdir(parents=True, exist_ok=True)

        output_path = destination / f"{run_name}_{num_runs}.parquet"
        pd.DataFrame(results).to_parquet(output_path, index=False)

    return results

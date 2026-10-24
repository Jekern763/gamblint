import sys
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
if str(CODE_DIR) not in sys.path:
    sys.path.append(str(CODE_DIR))

from algorithm_paths import (
    RAW_DATA_DIR,
    ensure_backend_importable,
)

# Add the backend root before importing its agent packages.
ensure_backend_importable()

from algorithm_paths import ensure_backend_importable

ensure_backend_importable()

from agent_algorithms.average_agent import AverageAgent
from agent_algorithms.constant_agent import ConstantAgent
from agent_algorithms.expectimax_agent import ExpectimaxAgent
from agent_algorithms.heuristic_agent import (
    GamblersFallacyAgent,
    InvariantAgent,
    ReflectionAgent,
)
from agent_algorithms.random_agent import RandomAgent
from agent_algorithms.single_path_agent import SinglePathAgent
from benchmark import benchmark

NUM_RUNS = 10_000


def main() -> None:
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    agents = {
        "random_agent": RandomAgent(1, 1),
        "reflection_agent": ReflectionAgent([0, 1, 0], 1, 1),
        "invariant_agent": InvariantAgent([0, 1, 0], 1, 1),
        "gamblers_fallacy_agent": GamblersFallacyAgent(1, 1),
        "single_path_agent": SinglePathAgent(1, 1),
        "expectimax_agent": ExpectimaxAgent(1, 1),
        "average_agent": AverageAgent(1, 1),
    }

    for name, agent in agents.items():
        benchmark(agent, name, NUM_RUNS, output_dir=RAW_DATA_DIR)

    for guess in range(2, 13):
        agent = ConstantAgent(1, 1, guess)
        benchmark(
            agent,
            f"constant_agent_{guess}",
            NUM_RUNS,
            output_dir=RAW_DATA_DIR,
        )


if __name__ == "__main__":
    main()

# Backend

This directory contains the core game logic, the algorithms that play the game, and the API used by the frontend. The backend is deployed as a Python AWS Lambda function, with API Gateway handling requests and DynamoDB storing game sessions.

## Conventions and Dependencies

To initialize this project, make sure you have Python 3.10+ and `uv` installed, and that you are located in the `backend` directory. Then run

```bash
uv sync --locked
```

This installs the project dependencies, including the development tools used for testing and linting.

To run the tests and checks, use

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

The CI workflow currently tests with Python 3.12 and 3.13.

## Overview

### `agent_algorithms/`

Contains the base `Agent` class and the different hand-written algorithms used to make guesses. These include simple baselines, heuristic approaches, and the Expectimax algorithm. For a comparison of their performance, see `research/algorithm_comparison/`.

### `game_engine/`

Contains the core game logic. `DepletingDice` implements the dice mechanic, `GameState` stores the current state of a game, and `Game` manages rolls, guesses, payouts, and serialization. The game engine is independent of the API and does not manage the overall game loop.

### `tests/`

Contains the pytest suite for the game engine, agent algorithms, database gateway, and API routes.

### Other files

- `app.py`: The AWS Lambda entry point and API. It exposes the `/start-game` and `/guess` routes, which are reached through the `/api/` path in the deployed application.
- `database_gateway.py`: Handles reading and writing game session data in DynamoDB.
- `models.py`: Defines the Pydantic request schemas and the data models used for database records.
- `init_local_db.py`, `reset_local_db.py`, and `peek_db.py`: Optional scripts for creating, resetting, and inspecting a local DynamoDB table. They connect to DynamoDB Local at `http://127.0.0.1:8000`, so a local instance must already be running. **The initialization and reset scripts delete the existing local table before recreating it.**
- `pyproject.toml` and `uv.lock`: Define the Python package, dependencies, and locked environment.

The local database scripts are only for development and testing. They are not required to run the deployed application or the automated test suite.

# Gamblint

A simple but original game mechanic, with surrounding research and infrastructure.

---

## Abstract

Gamblint (Gamble + Integer) is a probability-based game designed to study decision making under uncertainty. The project combines game design, probability theory, statistical analysis, cloud engineering, and more to conduct a rigourous and broad level of research

The game is a unique, simple dice game, with a twist. Every time a dice is rolled, that face is removed for the remainder of the round. It also incorporates the properties of two dice, to create a weighted probability curve which is the highest at 7. The player of the game has incomplete knowledge of what dice sides have been rolled, they only know the sum of the two dice.

For a visual aid, go to `research/interactive_graph/how_to.md` to learn how to set up. After that, you will be able to play around with the games simulation.

The project is extremely broad, and as such this README will not be able to touch on every aspect. Treat it as a shallow overview, there are more details available in every sub directory.

## Getting Started

This project is meant to be reproducable in most aspects. To get started, first make sure you have the proper dependencies installed, via uv and pnpm. First, make sure you have uv and pnpm installed with

`uv --version`
`pnpm --version`

then, from the project root

``` bash
cd backend
uv sync
cd ../research
uv sync
cd frontend
pnpm install --frozen-lockfile
```

Other external dependencies are

- Docker Desktop
- Node.js
- Python
- Javascript
- Typescript

---

## Project Goals

While the project began as a simple game mechanic, and a quick python program, its overarching goals have since become much larger, and interdisciplinary. While the game itself represents unique mathematics and statistics, the value can go much deeper. Overall, the project combines multiple areas of study:

- Game design

- Computer Science

- Frontend Design

- Platform Engineering (AWS CDK architecture)

- Mathematics  (stochastic and bayesian probability, combinatorics and discrete math)

- Statistics (Algorithm playstyle analysis)

- Scientific Research (Writing a scientific paper, professionally summarizing results)

### Technologies Used

- Python

- TypeScript

- JavaScript

- Vanilla HTML

- CSS

- AWS CDK

- GitHub Actions

- pytest/pytest-mock

- jest

- pnpm

- uv

Any setup necessary will be found in the README at the root of every child directory of this projet

---

### `backend/game_engine`

The game engine strictly adheres to Object Oriented Programing principles, along with separation of concerns. Within it is a python dataclass to represent the game state, a class to represent the unique dice system the game uses, and a class to represent the game as a whole. The game itself has no knowledge of any game loop, only its internal state and logic. It acts as the "physics" of the game, only setting bounds and returning outcomes. The game object takes 2 multipliers as arguments: riskiness multiplier and jackpot multiplier. It applies these with every payout calculation.

### `backend/agent_algorithms`

In total there are 8 algorithms (not including the constant baseline algorithm). Each one represents a different human play style, or the absolute baseline/ceiling of possible play. It is important to note that these agents are **not** artificial intelligence, but just hand coded algorithms that play the game in different ways. The algorithms use a game object, but cannot peek inside it to get the internal state, and therefore cannot "cheat". For a full analysis and comparison of these different algorithms, look at `research/algorithm_comparison`

### `backend/app.py`

The backend API is completely serverless. It is built an AWS Lambda Python Function, but traffic is routed to it through API Gateway. It does not track the gameloop, but has two simple routes

1. api/start-game: This simply initializes a game, storing a mid-session record to DynamoDB. It takes a jackpot multiplier and a riskiness multiplier as data, and returns the peeks and session_id
2. api/guess: This takes a guess, calculates payout, and saves the result to the database. It takes the guess, and a game object (as json) to then randomly generate the actual roll based on the current game state. It also does a small check for "cheating", where if the player has guessed the mathematically perfect roll multiple times in a row, it gets flagged.

### other files in `backend`

Some of these, such as `database_gateway.py`, `init_local_db.py`, and `peek_db.py` are just local testing scripts. They should not be necessary for this project to run, but should also still work on most personal computers with Docker Desktop installed.

### `frontend/*`

The frontend files are stored in an AWS S3 bucket, and served to the user via a cloudfront formation.  The frontend completely tracks the game loop itself, as well as keeping an user data stored in local storage. Because each round is independent any user data is completely cosmetic, such as net score or total rounds. The do however add a feeling of accomplishment for the player. After refactoring the scripts behind the frontend, there is now an object for storage, game state, and user interface.

### Infrastructure

``` mermaid
graph TB

subgraph Internet
    User([User])
    DNS["Route 53<br/>gamblint.jamesekern.com"]
end

subgraph AWS["AWS Infrastructure"]

    CF["CloudFront Distribution"]

    S3[(S3 Frontend File Storage)]

    API["API Gateway"]

    Lambda["Backend Lambda Function"]

    DB[(DynamoDB)]

    Logs[(CloudWatch Logs)]

    DNS --> CF

    CF -->|Frontend Files| S3
    CF -->|/api/*| API
    API --> Lambda
    Lambda <--> DB
    Lambda --> Logs

end

subgraph CICD["CI / CD"]

    GitHub["GitHub Actions"]

    CDK["AWS CDK"]

    Infra["Infrastructure Stack"]

    Frontend["Frontend Build"]

    GitHub --> CDK
    CDK --> Infra

    Infra --> CF
    Infra --> API
    Infra --> Lambda
    Infra --> DB
    Infra --> S3

    CDK --> Frontend
    Frontend --> S3

end

User --> DNS
```

### `research/*`

For this directory, there is simply too much work to put here. It is described in more detial in `research/README.md`. In brief, it is the multidisciplinary analysis of many aspects of the game, from algorithms to some tangential mathematics

---

## Development Practices

Throught development the project used the follwing practices:

- Object-Oriented Programming

- Type hints

- Formatting

- Dependency management with uv for python and pnpm for typescript and javascript

- Version Control via Github

- Complete tests for python, AWS CDK, and frontend

---

## Continuous Integration & Deployment

A github actions workflow was setup (in `.github/workflows`) to preserve any current working structure. In the workflow triggers were either on a pull request or on a push to main

- on: pull request
    1. linting and formatting
    2. Dependency checking
    3. Unit tests
    4. CDK synthesis check
- on: push to main
    1. Automatic CDK deployment
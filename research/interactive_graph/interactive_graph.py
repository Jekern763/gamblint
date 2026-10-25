import sys
from collections import Counter
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

project_root = Path(__file__).resolve().parent.parent.parent
backend_path = project_root / "backend"

sys.path.insert(0, str(backend_path))

from agent_algorithms.expectimax_agent import ExpectimaxAgent  # type: ignore

app = Flask(__name__, static_folder=".", static_url_path="")

MIN_ROLL = 2
MAX_ROLL = 12
MAX_PEEKS = 6


# --------------------------------------------------
# Calculation functions
# Add your actual math here later.
# --------------------------------------------------


def get_best_guess(peeks, riskiness, jackpot):
    if not peeks:
        return None

    agent = ExpectimaxAgent(riskiness, jackpot)
    agent.session.num_peeks = len(peeks)

    return agent.get_action(peeks)


def get_next_roll_distribution(peeks):

    initial_faces = tuple(range(1, 7))
    paths = []

    def search(index, die1, die2):
        if index == len(peeks):
            paths.append((die1, die2))
            return

        target = peeks[index]

        for a in die1:
            for b in die2:
                if a + b == target:
                    search(
                        index + 1,
                        tuple(x for x in die1 if x != a),
                        tuple(x for x in die2 if x != b),
                    )

    search(0, initial_faces, initial_faces)

    if not paths:
        return None

    counts = Counter()
    total_outcomes = 0

    for die1, die2 in paths:
        for a in die1:
            for b in die2:
                counts[a + b] += 1
                total_outcomes += 1

    return {
        "probabilities": {
            str(total): count / total_outcomes
            for total, count in sorted(counts.items())
        }
    }


# --------------------------------------------------
# Input validation
# --------------------------------------------------


def read_peeks():
    """Validate a JSON request containing a list of peeks."""
    body = request.get_json(silent=True)

    if not isinstance(body, dict):
        return None, (jsonify(error="Expected a JSON object."), 400)

    peeks = body.get("peeks")

    if not isinstance(peeks, list):
        return None, (jsonify(error="'peeks' must be an array."), 400)

    if len(peeks) > MAX_PEEKS:
        return None, (
            jsonify(error=f"At most {MAX_PEEKS} peeks are allowed."),
            400,
        )

    for index, value in enumerate(peeks):
        # bool is a subclass of int in Python, so reject it explicitly.
        if isinstance(value, bool) or not isinstance(value, int):
            return None, (
                jsonify(error=f"Peek {index + 1} must be an integer."),
                400,
            )

        if not MIN_ROLL <= value <= MAX_ROLL:
            return None, (
                jsonify(
                    error=(
                        f"Peek {index + 1} must be between {MIN_ROLL} and {MAX_ROLL}."
                    )
                ),
                400,
            )

    return peeks, None


# --------------------------------------------------
# Website route
# --------------------------------------------------


@app.get("/")
def index():
    return send_from_directory(".", "interactive_graph.html")


# --------------------------------------------------
# API: best guess
# --------------------------------------------------


@app.post("/api/best-guess")
def best_guess():
    peeks, error = read_peeks()

    if error:
        return error

    body = request.get_json(silent=True)
    riskiness = body.get("riskiness", 1.0)
    jackpot = body.get("jackpot", 1.0)

    for name, value in [
        ("riskiness", riskiness),
        ("jackpot", jackpot),
    ]:
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not 0 <= value <= 10
        ):
            return jsonify(error=f"'{name}' must be a number between 0 and 10."), 400

    result = get_best_guess(peeks, riskiness, jackpot)

    if result is None:
        return jsonify(
            error="Enter at least one peek to calculate a best guess.",
            code="not_implemented",
        ), 501

    if (
        isinstance(result, bool)
        or not isinstance(result, int)
        or not MIN_ROLL <= result <= MAX_ROLL
    ):
        app.logger.error(
            "get_best_guess returned an invalid result: %r",
            result,
        )
        return jsonify(error="The calculation returned an invalid best guess."), 500

    return jsonify(best_guess=result)


# --------------------------------------------------
# API: next-roll probability distribution
# --------------------------------------------------


@app.post("/api/next-roll-distribution")
def next_roll_distribution():
    peeks, error = read_peeks()

    if error:
        return error

    result = get_next_roll_distribution(peeks)

    if result is None:
        return jsonify(
            error="Distribution calculation has not been implemented yet.",
            code="not_implemented",
        ), 501

    if not isinstance(result, dict):
        app.logger.error("Distribution function returned a non-dictionary.")
        return jsonify(error="The calculation returned an invalid distribution."), 500

    probabilities = {}

    for roll in range(MIN_ROLL, MAX_ROLL + 1):
        probability = result["probabilities"].get(str(roll), 0.0)

        if (
            isinstance(probability, bool)
            or not isinstance(probability, (int, float))
            or not 0 <= probability <= 1
        ):
            app.logger.error("Invalid probability for roll %s: %r", roll, probability)
            return jsonify(
                error=f"The calculation returned an invalid probability for {roll}."
            ), 500

        probabilities[str(roll)] = probability

    return jsonify(probabilities=probabilities)


# --------------------------------------------------
# Start the local server
# --------------------------------------------------

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )

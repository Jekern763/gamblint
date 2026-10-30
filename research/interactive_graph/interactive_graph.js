const PEEK_COUNT = 6;
const MIN_VALUE = 2;
const MAX_VALUE = 12;
const DEFAULT_PEEK_VALUES = ["", "", "", "", "", ""];

const DEFAULT_PARAMETER = 1;
const PARAMETER_MIN = 0;
const PARAMETER_MAX = 10;
const PARAMETER_STEP = 0.01;

let latestRequestId = 0;
let updateTimer = null;

// Both the slider and number input now use the same actual 0–10 scale.
function positionToValue(value) {
  const number = Number(value);

  if (!Number.isFinite(number)) {
    return DEFAULT_PARAMETER;
  }

  return Math.min(PARAMETER_MAX, Math.max(PARAMETER_MIN, number));
}

// Clamp and round to the nearest hundredth.
function valueToPosition(value) {
  const number = Number(value);

  if (!Number.isFinite(number)) {
    return DEFAULT_PARAMETER.toFixed(2);
  }

  const bounded = Math.min(PARAMETER_MAX, Math.max(PARAMETER_MIN, number));

  return (Math.round(bounded / PARAMETER_STEP) * PARAMETER_STEP).toFixed(2);
}

function getParameterValue(name) {
  const slider = document.getElementById(`${name}-slider`);

  return Number(valueToPosition(slider.value));
}

function updateParameterLabels() {
  for (const name of ["riskiness", "jackpot"]) {
    const slider = document.getElementById(`${name}-slider`);
    const numberInput = document.getElementById(`${name}-value`);

    const value = Number(positionToValue(slider.value));

    // Avoid overwriting the field while the user is typing.
    if (document.activeElement !== numberInput) {
      numberInput.value = value.toFixed(2);
    }

    slider.setAttribute("aria-valuetext", value.toFixed(2));
  }
}

// --------------------------------------------------
// Chart rendering
// --------------------------------------------------

function renderChart(values = {}) {
  const chart = document.getElementById("bar-chart");

  const numbers = Array.from(
    { length: MAX_VALUE - MIN_VALUE + 1 },
    (_, index) => MIN_VALUE + index,
  );

  const percentages = Object.fromEntries(
    numbers.map((number) => [
      number,
      Math.max(0, Number(values[number]) || 0) * 100,
    ]),
  );

  const maxBarValue = Math.max(0.1, ...Object.values(percentages));

  // Create columns once so their heights can animate.
  if (chart.children.length === 0) {
    for (const number of numbers) {
      const column = document.createElement("div");
      column.className = "bar-column";
      column.dataset.number = String(number);

      const valueLabel = document.createElement("div");
      valueLabel.className = "bar-value";

      const track = document.createElement("div");
      track.className = "bar-track";

      const bar = document.createElement("div");
      bar.className = "bar";
      bar.setAttribute("aria-hidden", "true");

      track.append(bar);

      const label = document.createElement("div");
      label.className = "bar-label";
      label.textContent = String(number);

      column.append(valueLabel, track, label);
      chart.append(column);
    }
  }

  // Update existing columns rather than rebuilding the graph.
  for (const column of chart.children) {
    const number = Number(column.dataset.number);
    const value = percentages[number];

    column.querySelector(".bar-value").textContent = `${value.toFixed(1)}%`;

    column.querySelector(".bar").style.height =
      `${(value / maxBarValue) * 100}%`;
  }
}

// --------------------------------------------------
// Peek inputs
// --------------------------------------------------

function hasPeekValue(value) {
  if (value === "" || value === null || value === undefined) {
    return false;
  }

  const number = Number(value);

  return Number.isInteger(number) && number >= MIN_VALUE && number <= MAX_VALUE;
}

function getPeekValues() {
  return Array.from({ length: PEEK_COUNT }, (_, index) => {
    const input = document.getElementById(`peek-input-${index}`);
    return input ? input.value : "";
  });
}

function getValidPeeks() {
  const values = getPeekValues();
  const peeks = [];

  // Only accept consecutive peeks starting from the first field.
  for (const value of values) {
    if (!hasPeekValue(value)) {
      break;
    }

    peeks.push(Number(value));
  }

  return peeks;
}

function renderPeeks(values = DEFAULT_PEEK_VALUES) {
  const container = document.getElementById("input-slots");
  container.replaceChildren();

  for (let index = 0; index < PEEK_COUNT; index++) {
    const wrapper = document.createElement("div");
    wrapper.className = "slot";

    wrapper.classList.toggle(
      "is-disabled",
      index > 0 && !hasPeekValue(values[index - 1]),
    );

    const label = document.createElement("label");
    label.htmlFor = `peek-input-${index}`;
    label.textContent = `Peek ${index + 1}`;

    const input = document.createElement("input");
    input.id = `peek-input-${index}`;
    input.name = `peek-${index + 1}`;
    input.type = "number";
    input.min = String(MIN_VALUE);
    input.max = String(MAX_VALUE);
    input.step = "1";
    input.value = values[index] ?? "";
    input.placeholder = "2–12";
    input.inputMode = "numeric";

    input.disabled = index > 0 && !hasPeekValue(values[index - 1]);

    input.setAttribute(
      "aria-label",
      `Peek ${index + 1}, choose a number from 2 to 12`,
    );

    input.addEventListener("input", () => {
      const currentValues = getPeekValues();
      currentValues[index] = input.value;

      // Clearing a peek clears and locks all later peeks.
      if (input.value === "") {
        for (let later = index + 1; later < PEEK_COUNT; later++) {
          currentValues[later] = "";
        }
      }

      renderPeeks(currentValues);

      // Number inputs don't support setSelectionRange().
      document.getElementById(`peek-input-${index}`).focus();

      scheduleResultsUpdate();
    });

    input.addEventListener("change", () => {
      const currentValues = getPeekValues();

      if (input.value !== "") {
        const parsed = Number(input.value);

        currentValues[index] = String(
          Number.isFinite(parsed)
            ? Math.min(MAX_VALUE, Math.max(MIN_VALUE, Math.round(parsed)))
            : "",
        );
      }

      renderPeeks(currentValues);
      scheduleResultsUpdate();
    });

    wrapper.append(label, input);
    container.append(wrapper);
  }
}

// --------------------------------------------------
// Display helpers
// --------------------------------------------------

function setChartValues(probabilities) {
  renderChart(probabilities);
}

function setBestGuess(value) {
  const output = document.getElementById("best-guess-value");

  if (value === null || value === undefined || value === "") {
    output.textContent = "—";
    return;
  }

  const number = Number(value);

  output.textContent = Number.isFinite(number) ? String(number) : "—";
}

// --------------------------------------------------
// API requests
// --------------------------------------------------

function scheduleResultsUpdate() {
  // Invalidate requests already in flight.
  latestRequestId++;

  clearTimeout(updateTimer);

  // Brief debounce prevents excessive requests while typing or sliding.
  updateTimer = setTimeout(updateResults, 120);
}

async function updateResults() {
  const requestId = ++latestRequestId;
  const peeks = getValidPeeks();

  const riskiness = getParameterValue("riskiness");
  const jackpot = getParameterValue("jackpot");

  updateParameterLabels();

  const distributionBody = JSON.stringify({ peeks });

  const guessBody = JSON.stringify({
    peeks,
    riskiness,
    jackpot,
  });

  // Always request the distribution, including when peeks is empty.
  const distributionPromise = fetch("/api/next-roll-distribution", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: distributionBody,
  }).then(async (response) => {
    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        `Distribution API returned ${response.status}: ` + JSON.stringify(data),
      );
    }

    return data;
  });

  // No peeks means there is no best guess to calculate.
  // Avoid calling the endpoint in that state.
  const guessPromise =
    peeks.length > 0
      ? fetch("/api/best-guess", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: guessBody,
        }).then(async (response) => {
          const data = await response.json();

          if (!response.ok) {
            throw new Error(
              `Best-guess API returned ${response.status}: ` +
                JSON.stringify(data),
            );
          }

          return data;
        })
      : null;

  if (!guessPromise && requestId === latestRequestId) {
    setBestGuess(null);
  }

  // Update the graph independently of the best-guess calculation.
  try {
    const distributionData = await distributionPromise;

    if (requestId === latestRequestId) {
      setChartValues(distributionData.probabilities);
    }
  } catch (error) {
    console.error("Failed to update distribution:", error);

    if (requestId === latestRequestId) {
      renderChart({});
    }
  }

  if (guessPromise) {
    try {
      const guessData = await guessPromise;

      if (requestId === latestRequestId) {
        setBestGuess(guessData.best_guess);
      }
    } catch (error) {
      console.error("Failed to update best guess:", error);

      if (requestId === latestRequestId) {
        setBestGuess(null);
      }
    }
  }
}

// --------------------------------------------------
// Reset and initialization
// --------------------------------------------------

function resetPeeks() {
  renderPeeks(DEFAULT_PEEK_VALUES);
  scheduleResultsUpdate();
}

function initializeSliders() {
  for (const name of ["riskiness", "jackpot"]) {
    const slider = document.getElementById(`${name}-slider`);
    const numberInput = document.getElementById(`${name}-value`);

    // Enforce matching bounds and precision even if the HTML is stale.
    slider.min = String(PARAMETER_MIN);
    slider.max = String(PARAMETER_MAX);
    slider.step = String(PARAMETER_STEP);

    numberInput.min = String(PARAMETER_MIN);
    numberInput.max = String(PARAMETER_MAX);
    numberInput.step = String(PARAMETER_STEP);

    slider.value = valueToPosition(DEFAULT_PARAMETER);
    numberInput.value = DEFAULT_PARAMETER.toFixed(2);

    // Moving a slider updates its numeric field.
    slider.addEventListener("input", () => {
      updateParameterLabels();
      scheduleResultsUpdate();
    });

    // Typing a number updates the slider and triggers recalculation.
    numberInput.addEventListener("input", () => {
      const typedValue = numberInput.valueAsNumber;

      // Allow the user to temporarily clear the field while editing.
      if (!Number.isFinite(typedValue)) {
        return;
      }

      slider.value = valueToPosition(typedValue);

      updateParameterLabels();
      scheduleResultsUpdate();
    });

    // On commit, clamp the value and normalize it to two decimals.
    numberInput.addEventListener("change", () => {
      const typedValue = numberInput.valueAsNumber;

      if (!Number.isFinite(typedValue)) {
        numberInput.value = Number(slider.value).toFixed(2);
        updateParameterLabels();
        return;
      }

      slider.value = valueToPosition(typedValue);
      numberInput.value = Number(slider.value).toFixed(2);

      updateParameterLabels();
      scheduleResultsUpdate();
    });
  }

  updateParameterLabels();
}

document.getElementById("reset-button").addEventListener("click", resetPeeks);

initializeSliders();
renderChart({});
renderPeeks();
updateResults();

// Browser-console helpers.
window.setChartValues = setChartValues;
window.getPeekValues = getPeekValues;
window.setBestGuess = setBestGuess;
window.resetPeeks = resetPeeks;
window.updateResults = updateResults;
window.getParameterValue = getParameterValue;

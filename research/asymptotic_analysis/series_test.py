import pickle

import numpy as np
import pandas as pd

with open("generated_sequence.pkl", "rb") as file:
    data = pickle.load(file)

data = data[2]

df = pd.DataFrame(data).T.rename_axis(columns="n", index="t")


for index, row in df.iterrows():
    # Filter out NaN values from the current row
    valid_data = row.dropna()

    # Extract X (column headers) and Y (cell values)
    x = valid_data.index.astype(float)
    y = valid_data.values

    degree = int(index)

    # Check if there are enough data points to fit the polynomial
    if len(x) >= degree + 1:
        # Fit the data to get polynomial coefficients
        coeffs = np.polyfit(x, y, degree)

        # Convert to a formatted polynomial equation object
        poly_eq = np.poly1d(coeffs)

        print(f"A_{index}(n) = {poly_eq}" + f" for {tuple(row)}")

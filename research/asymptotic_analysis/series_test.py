"""
SERIES TO TAKE A LOOK AT:
- fix number of dice, increase number of sides
    - count of complete peek-histories
    - sequence of peek-histories over t
    - count of all peek-histories (sum of above)
- fix number of sides, increase number of dice
    - count of complete peek-histories
    - sequence of peek-histories over t
    - count of all peek-histories
    - correlate to figurate sequneces?
        n -> sides in 2d?
        d -> dimension?
"""

import sys

import pandas as pd

# adding path to specific objects found in the pickle file
sys.path.append("../game_analysis")

# pull in history df
df: pd.DataFrame = pd.read_pickle("../data/game_analysis/analysis_by_history.pkl")

max_sides = df["num_sides"].max()
max_dice = df["num_dice"].max()

# ==============================
# VARYING N, SETTING D = 2
# ==============================

num_dice_2 = df[df["num_dice"] == 2]

# 1. ORIGINAL VECTOR SUM SEQUENCE

counts = num_dice_2.query("depth == num_sides").groupby("num_sides").size()

vector_sum_sequence = [1] + [int(counts.get(i, 0)) for i in range(1, max_sides + 1)]

# 2. SEQUENCE OVER t

counts = num_dice_2.groupby(["num_sides", "depth"]).size()

partial_sum_sequence: list[list[int]] = [[1]] + [
    [1] + [int(counts.get((num_sides, depth), 0)) for depth in range(1, num_sides + 1)]
    for num_sides in range(1, max_sides + 1)
]

# 3. TOTAL COMPLETE AND INCOMPLETE HISTORIES

total_histories = [sum(x) for x in partial_sum_sequence]

# ==============================
# VARYING D, SETTING N = 1-6
# ==============================

# 1. COUNT OF COMPLETE HISTORIES

vector_sums_varied_d: dict[int, list[int]] = {}

filtered = df.query("depth == num_sides").groupby(["num_sides", "num_dice"]).size()

for num_sides in range(1, max_sides + 1):
    vector_sums_varied_d[num_sides] = [
        1 if num_dice == 0 else int(filtered.get((num_sides, num_dice), 0))
        for num_dice in range(max_dice + 1)
    ]

# 2. SEQUENCE OF PEEK HISTORIES OVER t

filtered = df.groupby(["num_sides", "num_dice", "depth"]).size()

partial_sum_sequence_varied_d: dict[int, list[list[int]]] = {}

for num_sides in range(1, max_sides + 1):
    partial_sum_sequence_varied_d[num_sides] = [
        [1]
        + [
            int(filtered.get((num_sides, num_dice, depth), 0))
            for depth in range(1, num_sides + 1)
        ]
        for num_dice in range(max_dice + 1)
    ]

# 3. TOTAL OF INCOMPLETE + COMPLETE HISTORIES OVER t

total_histories_varied_d: dict[int, list[int]] = {}

for num_sides in range(1, max_sides + 1):
    total_histories_varied_d[num_sides] = [
        sum(sequence) for sequence in partial_sum_sequence_varied_d[num_sides]
    ]


# ====================
# VARYING T AND N
# ====================

count_histories_by_depth_and_num_sides: list[list[int]]

# [depth][num_sides]
count = num_dice_2.groupby(["depth", "num_sides"]).size()

count_histories_by_depth_and_num_sides = [
    [0]
    + [int(count.get((depth, num_sides), 0)) for num_sides in range(1, max_sides + 1)]
    for depth in range(max_sides + 1)
]

for index, item in enumerate(count_histories_by_depth_and_num_sides):
    print(f"t={index}: {item}")

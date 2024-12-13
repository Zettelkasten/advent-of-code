# File format contains segments like this
"""
Button A: X+77, Y+52
Button B: X+14, Y+32
Prize: X=5233, Y=14652

Button A: ...
"""
from typing import List

import numpy as np

button_a: List[np.ndarray] = []
button_b: List[np.ndarray] = []
prices: List[np.ndarray] = []

def parse_list(l):
    a, b = l.split(", ")
    return np.array((int(a[2:]), int(b[2:])), dtype=np.int32)

with open("input", "rt") as input_file:
    data = input_file.read()
    segments = data.split("\n\n")
    for segment in segments:
        lines = segment.strip().splitlines()
        assert len(lines) == 3
        assert lines[0].startswith("Button A: ")
        assert lines[1].startswith("Button B: ")
        assert lines[2].startswith("Prize: ")
        button_a.append(parse_list(lines[0][len("Button A: "):]))
        button_b.append(parse_list(lines[1][len("Button B: "):]))
        prices.append(parse_list(lines[2][len("Prize: "):]))

assert len(button_a) == len(button_b) == len(prices)

result = 0

for a, b, price in zip(button_a, button_b, prices):
    # find integer r, s > 0 s.t. price = r * a + s * b
    sol = np.linalg.solve(np.array([a, b]).T, price)
    # round to nearest integer
    sol = np.round(sol)
    sol = sol.astype(np.int32)
    # check if it is correct
    if np.all(sol[0] * a + sol[1] * b == price) and np.all(sol >= 0):
        result += 3 * sol[0] + sol[1]

print(result)
import re

import numpy as np

with open("input", "rt") as input_file:
    lines = input_file.readlines()
positions = np.ndarray((len(lines), 2), dtype=np.int32)
velocities = np.ndarray((len(lines), 2), dtype=np.int32)
for line_num, line in enumerate(lines):
    pos_x, pos_y, vel_x, vel_y = re.match(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", line).groups()
    positions[line_num] = [int(pos_x), int(pos_y)]
    velocities[line_num] = [int(vel_x), int(vel_y)]

width = 101
height = 103
size = np.asarray((width, height))

def score(pos):
    quad_1 = np.count_nonzero((pos[:, 0] < (width - 1) / 2) & (pos[:, 1] < (height - 1) / 2))
    quad_2 = np.count_nonzero((pos[:, 0] < (width - 1) / 2) & (pos[:, 1] > (height - 1) / 2))
    quad_3 = np.count_nonzero((pos[:, 0] > (width - 1) / 2) & (pos[:, 1] < (height - 1) / 2))
    quad_4 = np.count_nonzero((pos[:, 0] > (width - 1) / 2) & (pos[:, 1] > (height - 1) / 2))
    return quad_1 * quad_2 * quad_3 * quad_4

print(score((positions + 100 * velocities) % size))

new_positions = positions

for step in range(1, 10_000):
    new_positions = (new_positions + velocities) % size

    std = np.std(new_positions, axis=0)
    if np.sum(std) < 40:
        print("=" * 100)
        picture = np.zeros(size, dtype=np.int32)
        for pos in new_positions:
            picture[*pos] += 1

        print(step, std)
        for y in range(height):
            for x in range(width):
                print(min(picture[x, y], 9) if picture[x, y] > 0 else " ", end="")
            print()
        print()
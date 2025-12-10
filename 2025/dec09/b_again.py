import math
from tqdm import tqdm
import numpy

small = False

pairs = [line.strip().split(",") for line in open("input" + ("_small" if small else ""))]
pairs_list = [(int(x), int(y)) for x, y in pairs]
pairs = numpy.asarray(pairs_list, dtype=int)
num_points = pairs.shape[0]

pairs_orig_coords = pairs.copy()

unique_xs = sorted(numpy.unique(pairs[:, 0]))
unique_ys = sorted(numpy.unique(pairs[:, 1]))

# minify
new_pairs_list = []
for (x, y) in pairs_list:
    new_pairs_list.append((unique_xs.index(x), unique_ys.index(y)))
pairs_list = new_pairs_list
del new_pairs_list

pairs = numpy.asarray(pairs_list, dtype=int)


max_x = max(x for (x, y) in pairs)
max_y = max(y for (x, y) in pairs)

grid = set()
for point, next_point in zip(pairs_list, pairs_list[1:] + pairs_list[:1]):
    point, next_point = min(point, next_point), max(point, next_point)
    grid.add(point)
    if point[0] == next_point[0]:
        for y in range(point[1], next_point[1] + 1):
            grid.add((point[0], y))
    elif point[1] == next_point[1]:
        for x in range(point[0], next_point[0] + 1):
            grid.add((x, point[1]))
    else:
        assert False

to_fill = {(pairs_list[0][1] - 5, pairs_list[1][1])}
print(to_fill)
while len(to_fill) > 0:
    (x, y) = to_fill.pop()
    if (x, y) in grid:
        continue
    grid.add((x, y))
    to_fill.add((x + 1, y))
    to_fill.add((x - 1, y))
    to_fill.add((x, y - 1))
    to_fill.add((x, y + 1))

# fill the middle
for y in list(range(max_y + 1))[::-1]:
    for x in range(max_x + 1):
        # print(str(pairs_list.index((x, y)))[:1] if (x, y) in pairs_list else " ", end="")
        print("X" if (x, y) in grid else " ", end="")
    print()
print("----")


def area(i, j):
    # check if it's valid
    point_a, point_b = pairs[i], pairs[j]

    for x in range(min(point_a[0], point_b[0]), max(point_a[0], point_b[0]) + 1):
        for y in range(min(point_a[1], point_b[1]), max(point_a[1], point_b[1]) + 1):
            if (x, y) not in grid:
                return -1

    res = (math.fabs(pairs_orig_coords[i][0] - pairs_orig_coords[j][0]) + 1) * (math.fabs(pairs_orig_coords[i][1] - pairs_orig_coords[j][1]) + 1)
    return res

print(max(area(i, j) for i in tqdm(range(len(pairs))) for j in range(len(pairs)) if i < j))
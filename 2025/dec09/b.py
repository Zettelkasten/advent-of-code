import math
from tqdm import tqdm
import numpy

small = False

pairs = [line.strip().split(",") for line in open("input" + ("_small" if small else ""))]
pairs_list = [(int(x), int(y)) for x, y in pairs]
pairs = numpy.asarray(pairs_list, dtype=int)
num_points = pairs.shape[0]


max_x = max(x for x, y in pairs)
max_y = max(y for x, y in pairs)

grid = set()
for point, next_point in zip(pairs_list, pairs_list[1:] + pairs_list[:1]):
    point, next_point = min(point, next_point), max(point, next_point)
    grid.add(point)
    # if point[0] == next_point[0]:
    #     for y in range(point[1], next_point[1] + 1):
    #         grid.add((point[0], y))
    # elif point[1] == next_point[1]:
    #     for x in range(point[0], next_point[0] + 1):
    #         grid.add((x, point[1]))
    # else:
    #     assert False

for (x, y) in grid:
    assert not ((x - 1, y - 1) in grid or (x + 1, y - 1) in grid or (x + 1, y + 1) in grid or (x - 1, y + 1) in grid)

if small:
    for y in list(range(max_y + 1))[::-1]:
        for x in range(max_x + 1):
            print(str(pairs_list.index((x, y)))[:1] if (x, y) in pairs_list else " ", end="")
        print()
    print("----")

# fill the middle

SIGNS_SORTED = [
    (1, 0),  #  right
    (1, 1),  # right up
    (0, 1),  # up
    (-1, 1),  # up left
    (-1, 0),  # left
    (-1, -1),  # down left
    (0, -1),  # down
    (1, -1),  # down right
]

def my_tuple(np_arr):
    return (int(np_arr[0]), int(np_arr[1]))

def get_valid_quadrants(i, check_other_i):
    p_self = pairs[i]
    p_before = pairs[(i - 1) % num_points]
    p_after = pairs[(i + 1) % num_points]
    p_check = pairs[check_other_i]

    in_diff = my_tuple(numpy.sign(p_before - p_self))
    out_diff = my_tuple(numpy.sign(p_after - p_self))
    check_diff = my_tuple(numpy.sign(p_check - p_self))

    in_idx = SIGNS_SORTED.index(in_diff)
    out_idx = SIGNS_SORTED.index(out_diff)
    check_idx = SIGNS_SORTED.index(check_diff)

    assert in_idx != out_idx
    return (out_idx <= check_idx <= in_idx) or (in_idx <= out_idx <= check_idx) or (check_idx <= in_idx <= out_idx)

if small:
    assert get_valid_quadrants(1, 7)
    assert get_valid_quadrants(7, 1)

    assert not get_valid_quadrants(3, 5)
    assert not get_valid_quadrants(5, 3)

    assert get_valid_quadrants(2, 4)
    assert get_valid_quadrants(4, 2)

    assert get_valid_quadrants(3, 4)
    assert get_valid_quadrants(4, 3)

    assert not get_valid_quadrants(3, 5)
    assert not get_valid_quadrants(5, 3)

    assert not get_valid_quadrants(6, 0)
    assert not get_valid_quadrants(0, 6)

    assert get_valid_quadrants(5, 1)
    assert get_valid_quadrants(1, 5)

def area(i, j):
    # check if it's valid
    point_a, point_b = pairs[i], pairs[j]
    # check if it's generally okay
    if not get_valid_quadrants(i, j):
        return -1
    if not get_valid_quadrants(j, i):
        return -1

    # check ear clipping
    for k in range(len(pairs)):
        if k == i or k == j:
            continue
        point_test = pairs[k]
        if min(point_a[0], point_b[0]) < point_test[0] < max(point_a[0], point_b[0]) \
                and min(point_a[1], point_b[1]) < point_test[1] < max(point_a[1], point_b[1]):
            return -1

    res = (math.fabs(pairs[i][0] - pairs[j][0]) + 1) * (math.fabs(pairs[i][1] - pairs[j][1]) + 1)
    return res

print(max(area(i, j) for i in tqdm(range(len(pairs))) for j in range(len(pairs)) if i < j))
from collections import Counter

from tqdm import tqdm

input_grid = {}
with open("input", "rt") as input_file:
    for line_num, line in enumerate(input_file.readlines()):
        for col_num, char in enumerate(line.strip()):
            input_grid[(col_num, line_num)] = char

# find the start
start = [(x, y) for (x, y), val in input_grid.items() if val == "S"]
assert len(start) == 1
start_x, start_y = start[0]
input_grid[(start_x, start_y)] = "."

# find the end
end = [(x, y) for (x, y), val in input_grid.items() if val == "E"]
assert len(end) == 1
end_x, end_y = end[0]
input_grid[(end_x, end_y)] = "."

# trace the path through the maze
directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
path = []
next_x, next_y = start_x, start_y
while (next_x, next_y) != (end_x, end_y):
    path.append((next_x, next_y))
    # find neighbors
    neighbors = [(next_x + dir_x, next_y + dir_y) for (dir_x, dir_y) in directions]
    neighbors = [(x, y) for (x, y) in neighbors if input_grid[(x, y)] == "." and (x, y) not in path]
    assert len(neighbors) == 1
    next_x, next_y = neighbors[0]
path.append((end_x, end_y))

def neighbors(start, remaining_length, exclude) -> dict[tuple[int, int], int]:
    tiles = {(x + dir_x, y + dir_y): dist + 1 for (x, y), dist in start.items() for dir_x, dir_y in directions}
    goal_tiles = {
        (x, y): dist for (x, y), dist in tiles.items() if (x,y) in input_grid and input_grid[(x, y)] == "." and (x, y) not in exclude}

    if remaining_length > 1:
        further_tiles = {
            (x, y): dist for (x, y), dist in tiles.items() if (x, y) in input_grid and input_grid[(x, y)] in ".#" and (x, y) not in exclude}
        new_neighbors = neighbors(further_tiles, remaining_length=remaining_length - 1, exclude=goal_tiles.keys() | further_tiles.keys() | exclude)
        assert not (goal_tiles.keys() & new_neighbors.keys())
        return {**goal_tiles, **new_neighbors}
    else:
        return goal_tiles


def print_map(input_grid):
    width = max(x for x, y in input_grid) + 1
    height = max(y for x, y in input_grid) + 1
    for y in range(height):
        for x in range(width):
            print(input_grid[(x, y)], end="")
        print()

shortcut_counts_by_length = Counter()

for from_path, (path_x, path_y) in enumerate(tqdm(path)):
    for (shortcut_to_x, shortcut_to_y), dist in neighbors({(path_x, path_y): 0}, remaining_length=20, exclude=set()).items():
        to_path = path.index((shortcut_to_x, shortcut_to_y))
        shortcut_gain = (to_path - from_path) - dist
        # if shortcut_gain >= 100:
        #     print("This shortcut saves", shortcut_gain, "tiles and has a length of", dist)
        #     print_map({**input_grid, (path_x, path_y): "X", (shortcut_to_x, shortcut_to_y): "Y"})
        #     print()
        shortcut_counts_by_length[shortcut_gain] += 1

for length in sorted(shortcut_counts_by_length.keys()):
    print("Shortcuts of length", length, ":", shortcut_counts_by_length[length], "times")

print("There are so many shortcuts that save 100 tiles or more", sum(v for k, v in shortcut_counts_by_length.items() if k >= 100), "times")
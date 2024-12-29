import copy

from tqdm import tqdm

with open("input", "rt") as input_file:
    grid = [list(line.strip()) for line in input_file.readlines()]

height = len(grid)
width = len(grid[0])
grid = {(x, y): val for y, line in enumerate(grid) for x, val in enumerate(line)}

dir_map = {
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
    "^": (0, -1)
}
dirs_list = list(dir_map.keys())  # in order of turning right

# find the start position
start_pos = [pos for pos, val in grid.items() if val in dir_map]
assert len(start_pos) == 1
start_dir = grid[start_pos[0]]
start_x, start_y = start_pos[0]
del start_pos
grid[(start_x, start_y)] = "."


def print_map(grid):
    for y in range(height):
        for x in range(width):
            print(grid[(x, y)], end="")
        print()
    print()


# simulate ...
def simulation(grid, start_x, start_y, direction):
    visited_tiles_and_dirs = set()
    while True:
        dir_x, dir_y = dir_map[direction]
        next_x, next_y = start_x + dir_x, start_y + dir_y
        if (next_x, next_y) not in grid:
            return False
        elif grid[(next_x, next_y)] == "#":
            # turn
            direction = dirs_list[(dirs_list.index(direction) + 1) % len(dirs_list)]
        elif grid[(next_x, next_y)] == ".":
            # walk
            start_x += dir_x
            start_y += dir_y
        else:
            assert False
        if (start_x, start_y, direction) in visited_tiles_and_dirs:
            return True  # this leads to a loop!
        visited_tiles_and_dirs.add((start_x, start_y, direction))

count = 0

for x, y in tqdm(grid.keys()):
    if (x, y) != (start_x, start_y):
        grid_copy = grid.copy()
        grid_copy[(x, y)] = "#"
        if simulation(grid_copy, start_x, start_y, start_dir):
            count += 1

print(count)
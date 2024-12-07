import copy

with open("input", "rt") as input_file:
    grid = [list(line.strip()) for line in input_file.readlines()]

dirs_to_row_col = {
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1),
    "^": (-1, 0)
}
dirs_list = list(dirs_to_row_col.keys())  # in order of turning right

num_rows = len(grid)
num_cols = len(grid[0])

# simulate ...
def simulation(grid, start_row, start_col, dir, count_loops: bool):
    # returns -1 if stuck in a loop
    tiles_visited = 1
    loops_found = 0
    assert grid[start_row][start_col] == dir

    while True:
        row_dir, col_dir = dirs_to_row_col[dir]
        start_row += row_dir
        start_col += col_dir

        if not (0 <= start_row < num_rows and 0 <= start_col < num_cols):
            # ran away
            break

        if count_loops:
            grid_with_obstacle = copy.deepcopy(grid)
            grid_with_obstacle[start_row][start_col] = "#"  # place obstacle
            tiles_visited_with_obstacle, _ = simulation(
                grid_with_obstacle,
                start_row - row_dir, start_col - col_dir,  # backtrace to position before
                dir, count_loops=False)
            if tiles_visited_with_obstacle == -1:  # code for stuck in loop
                loops_found += 1
                print("This one has a loop when an obstacle is placed at", (start_row, start_col))

        new_ground = grid[start_row][start_col]
        if new_ground == "#":
            # need to turn
            start_row -= row_dir  # hacky backtrace ..
            start_col -= col_dir

            # turn
            dir = dirs_list[(dirs_list.index(dir) + 1) % len(dirs_list)]
            row_dir, col_dir = dirs_to_row_col[dir]

            # turn for realz
            start_row += row_dir
            start_col += col_dir
            new_ground = grid[start_row][start_col]
            if new_ground == "#":
                # this should only happen if we go into an dead end because
                # of a poorly placed obstacle.
                # I'm not sure if that's allowed, but let's just quit then...
                return tiles_visited, 0

        # explicitly no "else" here ...
        if new_ground in dirs_to_row_col:
            # was here before, do not count again.
            # but check if we are stuck in a loop.
            if grid[start_row][start_col] == dir:
                return -1, 0
            else:
                # update direction if we go there twice.
                # the last direction is the important one when counting loops
                grid[start_row][start_col] = dir

        elif new_ground == ".":
            # go here first time
            grid[start_row][start_col] = dir
            tiles_visited += 1
        else:
            assert False, new_ground

        if count_loops:
            print("\n".join("".join(row) for row in grid))
            print()

    return tiles_visited, loops_found

# find start position
start_row = min(i for i, row in enumerate(grid) if "^" in row)
start_col = grid[start_row].index("^")
dir = "^"

print(simulation(grid, start_row, start_col, dir, count_loops=True))

# idea for b:
# at any given position, simply try to place the obstacle in front once
with open("small_input", "rt") as input_file:
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

# find start position
start_row = min(i for i, row in enumerate(grid) if "^" in row)
start_col = grid[start_row].index("^")
dir = "^"

tiles_visited = 1
grid[start_row][start_col] = dir

# simulate ...
while True:
    row_dir, col_dir = dirs_to_row_col[dir]
    start_row += row_dir
    start_col += col_dir
    if not (0 <= start_row < num_rows and 0 <= start_col < num_cols):
        # ran away
        break
    else:
        new_ground = grid[start_row][start_col]
        if new_ground == "#":
            # need to turn
            start_row -= row_dir  # hacky backtrace ..
            start_col -= col_dir

            # turn
            dir = dirs_list[(dirs_list.index(dir) + 1) % len(dirs_list)]
            row_dir, col_dir = dirs_to_row_col[dir]
            # update tile with new direction for consistency
            grid[start_row][start_col] = dir

            # turn for realz
            start_row += row_dir
            start_col += col_dir
            new_ground = grid[start_row][start_col]
            assert new_ground != "#"

        # explicitly no "else" here ...
        if new_ground in dirs_to_row_col:
            # was here before, do not count again
            pass
        elif new_ground == ".":
            # go here first time
            grid[start_row][start_col] = dir
            tiles_visited += 1
        else:
            assert False, new_ground

    print("\n".join("".join(row) for row in grid))
    print()

print(tiles_visited)
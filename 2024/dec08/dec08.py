input_grid = []
with open("input", "rt") as input_file:
    for input_line in input_file.readlines():
        input_grid.append(input_line.strip())

num_rows = len(input_grid)
num_cols = len(input_grid[0])

antenna_row_cols = {}
for row_num, row in enumerate(input_grid):
    for col_num, val in enumerate(row):
        if val != ".":
            if val not in antenna_row_cols:
                antenna_row_cols[val] = []
            antenna_row_cols[val].append((row_num, col_num))

def calc_pos(a, diff, i):
    # return a + i * diff
    return (a[0] + i * diff[0], a[1] + i * diff[1])


def in_bounds(p):
    return 0 <= p[0] < num_rows and 0 <= p[1] < num_cols

antinode_row_cols = set()
for sender, row_cols in antenna_row_cols.items():
    for a_row_col in row_cols:
        for b_row_col in row_cols:
            if a_row_col == b_row_col:
                continue
            # a + (a - b) = 2a - b
            new_row_col = (2 * a_row_col[0] - b_row_col[0], 2 * a_row_col[1] - b_row_col[1])
            diff = (a_row_col[0] - b_row_col[0], a_row_col[1] - b_row_col[1])

            i = 0
            while in_bounds(calc_pos(a_row_col, diff, i)):
                antinode_row_cols.add(calc_pos(a_row_col, diff, i))
                i += 1
            i = -1
            while in_bounds(calc_pos(a_row_col, diff, i)):
                antinode_row_cols.add(calc_pos(a_row_col, diff, i))
                i -= 1

for row_num, row in enumerate(input_grid):
    for col_num, val in enumerate(row):
        if (row_num, col_num) in antinode_row_cols:
            print("#", end="")
        else:
            print(val, end="")
    print()


print(len(antinode_row_cols))
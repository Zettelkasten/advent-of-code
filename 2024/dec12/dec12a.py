area_per_letter = {}
perimiter_per_letter = {}

with open("input", "rt") as input_file:
    grid = [list(line.strip()) for line in input_file]
width = len(grid[0])
height = len(grid)
grid = {(x, y): grid[y][x] for x in range(width) for y in range(height)}

unseen_grid = grid.copy()
result = 0

while len(unseen_grid) > 0:
    # pick any grid tile
    x, y = next(iter(unseen_grid.keys()))
    val = grid[(x, y)]

    area = 0
    perimeter = 0

    # iterate through all neighbors
    neighbor_stack = [(x, y)]
    while len(neighbor_stack) > 0:
        x, y = neighbor_stack.pop()
        if (x, y) not in unseen_grid:  # already seen, don't go there again
            continue
        del unseen_grid[(x, y)]

        area += 1
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if grid.get((x + dx, y + dy)) == val:
                neighbor_stack.append((x + dx, y + dy))
            else:
                perimeter += 1

    result += area * perimeter
    print(val, area, perimeter)

print(result)
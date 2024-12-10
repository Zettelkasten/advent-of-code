with open("input", "rt") as input_file:
    grid = [line.strip() for line in input_file.readlines()]
    width = len(grid[0])
    height = len(grid)
    grid = {(x, y): int(c) for y, row in enumerate(grid) for x, c in enumerate(row)}


score = 0
for x, y in grid.keys():
    if grid[(x,y)] != 0:
        continue
    search_at = [(x, y)]
    for height in range(1, 10):
        next_search_at = set()
        neighbors = [(x + dir_x, y + dir_y) for x, y in search_at for dir_x, dir_y in [(0, 1), (1, 0), (0, -1), (-1, 0)]]
        search_at = [(x1, y1) for x1, y1 in neighbors if grid.get((x1, y1), -1) == height]
    print((x, y), "->", search_at)
    score += len(search_at)

print(score)
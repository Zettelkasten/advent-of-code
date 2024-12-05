with open("input", "rt") as file:
    rows = [line.strip() for line in file.readlines()]

width = len(rows[0])
height = len(rows)
assert all(len(r) == width for r in rows)

query = "XMAS"
counts = 0
for start_i, start_j in [(i, j) for i in range(width) for j in range(height)]:
    for dir_i, dir_j in [(i, j) for i in [-1, 0, 1] for j in [-1, 0, 1] if not (i == j == 0)]:
        okay = True
        for beam_length, beam_char in enumerate(query):
            i, j = start_i + beam_length * dir_i, start_j + beam_length * dir_j
            if not (0 <= i < width) or not (0 <= j < height):
                okay = False
                break
            if rows[j][i] != beam_char:
                okay = False
                break
        if okay:
            counts += 1

print(counts)

overall_count = 0
for start_i, start_j in [(i, j) for i in range(1, width - 1) for j in range(1, height - 1)]:
    if rows[start_j][start_i] != "A":
        continue
    found_count = 0
    for dir_i, dir_j in [(i, j) for i in [-1, 0, 1] for j in [-1, 0, 1] if not (i == j == 0) and (i + j) % 2 == 0]:
        i0, j0 = start_i + dir_i, start_j + dir_j
        i1, j1 = start_i - dir_i, start_j - dir_j
        if rows[j0][i0] == "M" and rows[j1][i1] == "S":
            found_count += 1
    assert found_count <= 2
    if found_count == 2:
        overall_count += 1

print(overall_count)
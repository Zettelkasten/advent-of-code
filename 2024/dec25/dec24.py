import numpy

locks = []
pins = []

with open("input", "rt") as input_file:
    lines = [l.strip() for l in input_file.readlines()]
    line_num = 0
    res = []
    while line_num < len(lines):
        lock = lines[line_num:line_num + 7]
        print(lock)

        if lock[0] == "#####":
            res = []
            for col in range(len(lock[0])):
                res.append(min(row for row in range(7) if lock[row][col] == ".") - 1)
            locks.append(numpy.asarray(res))
        else:
            res = []
            for col in range(len(lock[0])):
                res.append(5 - max(row for row in range(7) if lock[row][col] == "."))
            pins.append(numpy.asarray(res))

        line_num += 8

res = 0
for lock in locks:
    for pin in pins:
        if numpy.all(lock + pin <= 5):
            res += 1

print(res)

map = {}
height = 0
length = 0

movements = []

with open("input", "rt") as input_file:
    read_movements = False
    for line in input_file.readlines():
        line = line.strip()
        if line == "":
            assert not read_movements
            read_movements = True
        else:
            if read_movements:
                movements.extend(list(line))
            else:
                # read map
                if length == 0:
                    length = len(line)
                else:
                    assert length == len(line)
                row = height
                for col, c in enumerate(line):
                    map[(col, row)] = c
                height += 1

print(len(movements))

# find and then remove robot
robot_pos = [(x, y) for (x, y), val in map.items() if val == "@"]
assert len(robot_pos) == 1
robot_x, robot_y = robot_pos[0]
map[(robot_x, robot_y)] = "."
del robot_pos

dir_to_x_y = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}

for movement in movements:
    # attempt to push
    dir_x, dir_y = dir_to_x_y[movement]

    push_strength = 0
    # first, push through all "." and "O".
    while (next_tile := map[(robot_x + (push_strength + 1) * dir_x), (robot_y + (push_strength + 1) * dir_y)]) in ".O":
        push_strength += 1
        if next_tile == ".":
            break

    print(movement, push_strength, next_tile)
    if next_tile != "#":
        # we can actually push, do it!

        for length in reversed(range(1, push_strength)):
            push_from_x, push_from_y = (robot_x + length * dir_x), (robot_y + length * dir_y)
            push_to_x, push_to_y = push_from_x + dir_x, push_from_y + dir_y
            assert map[(push_to_x, push_to_y)] == "."
            map[(push_to_x, push_to_y)] = map[(push_from_x, push_from_y)]
            map[(push_from_x, push_from_y)] = "."

        robot_x += dir_x
        robot_y += dir_y

print(sum(100 * y + x for (x, y), val in map.items() if val == "O"))
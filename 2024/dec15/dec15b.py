
map = {}
height = 0
width = 0

movements = []

with open("input", "rt") as input_file:
    read_movements = False
    for line in input_file.readlines():
        line = line.strip()
        line = line.replace("#", "##")
        line = line.replace(".", "..")
        line = line.replace("O", "[]")
        line = line.replace("@", "@.")
        if line == "":
            assert not read_movements
            read_movements = True
        else:
            if read_movements:
                movements.extend(list(line))
            else:
                # read map
                if width == 0:
                    width = len(line)
                else:
                    assert width == len(line)
                row = height
                for col, c in enumerate(line):
                    map[(col, row)] = c
                height += 1

# find and then remove robot
robot_pos = [(x, y) for (x, y), val in map.items() if val == "@"]
assert len(robot_pos) == 1
robot_x, robot_y = robot_pos[0]
map[(robot_x, robot_y)] = "."
del robot_pos

dir_to_x_y = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}

def can_push(robot_x, robot_y, dir_x, dir_y, do_push: bool):
    new_x, new_y = robot_x + dir_x, robot_y + dir_y
    new_tile = map[(new_x, new_y)]
    if new_tile == ".":
        if do_push:
            map[(new_x, new_y)] = map[(robot_x, robot_y)]
            map[(robot_x, robot_y)] = "."
        return True
    elif new_tile == "#":
        assert not do_push
        return False
    elif new_tile in "[]":
        if dir_y == 0:  # horizontal
            push_further = can_push(robot_x + dir_x, robot_y + dir_y, dir_x, dir_y, do_push=do_push)
            if do_push:
                assert push_further
                map[(new_x, new_y)] = map[(robot_x, robot_y)]
                map[(robot_x, robot_y)] = "."
            return push_further
        elif dir_x == 0:  # vertical
            if new_tile == "[":
                # also need to push one to the right
                neighbor_x = 1
            elif new_tile == "]":
                # also need to push one to the left
                neighbor_x = -1
            else:
                assert False, new_tile
            push_further = can_push(robot_x + dir_x, robot_y + dir_y, dir_x, dir_y, do_push=do_push) and can_push(
                robot_x + dir_x + neighbor_x, robot_y + dir_y, dir_x, dir_y, do_push=do_push)
            if do_push:
                assert push_further
                map[(new_x, new_y)] = map[(robot_x, robot_y)]
                map[(robot_x, robot_y)] = "."
                map[(new_x + neighbor_x, new_y)] = map[(robot_x + neighbor_x, robot_y)]
                map[(robot_x + neighbor_x, robot_y)] = "."
            return push_further
    else:
        assert False

for movement in movements:
    # print the map
    for y in range(height):
        for x in range(width):
            print(map[(x, y)] if (x, y) != (robot_x, robot_y) else "@", end="")
        print()
    print("=" * 100)
    print("Want to push", movement)
    print()

    # attempt to push
    dir_x, dir_y = dir_to_x_y[movement]

    if can_push(robot_x, robot_y, dir_x, dir_y, do_push=False):
        print("can push")
        can_push(robot_x, robot_y, dir_x, dir_y, do_push=True)
        robot_x += dir_x
        robot_y += dir_y
    else:
        print("cannot push")


print(sum(100 * y + x for (x, y), val in map.items() if val == "["))
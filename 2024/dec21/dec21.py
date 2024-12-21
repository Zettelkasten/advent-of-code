from __future__ import annotations
import dataclasses
import re
from typing import Iterable


@dataclasses.dataclass(slots=True)
class Tile:
    a_key_pressed_list: str
    b_directional_pos: (int, int)  # robot 1 (directional)
    c_directional_pos: (int, int)  # robot 2 (directional)
    d_numeric_pos: (int, int)  # robot 3 (numerical)
    d_outputs_written: str
    previous_tile: Tile | None = dataclasses.field(repr=False)

    def __hash__(self):
        return hash((self.b_directional_pos, self.c_directional_pos, self.d_numeric_pos, self.d_outputs_written))

    def __eq__(self, other):
        if not isinstance(other, Tile):
            return False
        return (self.b_directional_pos, self.c_directional_pos, self.d_numeric_pos, self.d_outputs_written) == (other.b_directional_pos, other.c_directional_pos, other.d_numeric_pos, other.d_outputs_written)

all_directions = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}

directional_key_pad = {
    (1, 0): "^",
    (2, 0): "A",
    (0, 1): "<",
    (1, 1): "v",
    (2, 1): ">"
}
numeric_key_pad = {
    (0, 0): "7",
    (1, 0): "8",
    (2, 0): "9",
    (0, 1): "4",
    (1, 1): "5",
    (2, 1): "6",
    (0, 2): "1",
    (1, 2): "2",
    (2, 2): "3",
    (1, 3): "0",
    (2, 3): "A"
}

directional_keys_to_dir = {key: (x, y) for (x, y), key in directional_key_pad.items()}
numeric_keys_to_dir = {key: (x, y) for (x, y), key in numeric_key_pad.items()}


def do_search(target_d_outputs: str) -> Tile:
    initial_pos = Tile(
        a_key_pressed_list="", b_directional_pos=(2, 0), c_directional_pos=(2, 0),
        d_numeric_pos=(2, 3), d_outputs_written="", previous_tile=None)

    visited_tiles: set[Tile] = set()
    explore_tiles_to_cost: list[Tile] = [initial_pos]

    def tile_score(tile: Tile):
        already_used = len(tile.a_key_pressed_list)
        return already_used
        # other_outputs_to_write = len(target_d_outputs) - len(tile.d_outputs_written)
        # return already_used + other_outputs_to_write

    while True:
        # find tile with the lowest cost
        current_tile = min(explore_tiles_to_cost, key=tile_score)
        explore_tiles_to_cost.remove(current_tile)
        visited_tiles.add(current_tile)


        needed_d_key = target_d_outputs[len(current_tile.d_outputs_written)]

        # find the next tiles
        for a_key in directional_key_pad.values():
            next_d_outputs_written = current_tile.d_outputs_written

            b_x, b_y = current_tile.b_directional_pos
            if a_key == "A":
                # press button on B
                b_key = directional_key_pad[(b_x, b_y)]
                c_x, c_y = current_tile.c_directional_pos
                if b_key == "A":
                    # press button on C
                    c_key = directional_key_pad[(c_x, c_y)]
                    d_x, d_y = current_tile.d_numeric_pos
                    if c_key == "A":
                        # output
                        d_key = numeric_key_pad[(d_x, d_y)]
                        if d_key != needed_d_key:
                            continue
                        else:
                            next_d_outputs_written += d_key
                    else:
                        # move
                        d_dir_x, d_dir_y = all_directions[c_key]
                        d_x += d_dir_x
                        d_y += d_dir_y
                        if (d_x, d_y) not in numeric_key_pad:
                            continue
                else:
                    # move
                    c_dir_x, c_dir_y = all_directions[b_key]
                    c_x += c_dir_x
                    c_y += c_dir_y
                    if (c_x, c_y) not in directional_key_pad:
                        continue
                    d_x, d_y = current_tile.d_numeric_pos  # stays the same
            else:  # move
                b_dir_x, b_dir_y = all_directions[a_key]
                b_x += b_dir_x
                b_y += b_dir_y
                if (b_x, b_y) not in directional_key_pad:
                    continue
                c_x, c_y = current_tile.c_directional_pos  # stays the same
                d_x, d_y = current_tile.d_numeric_pos  # stays the same

            next_tile = Tile(
                a_key_pressed_list=current_tile.a_key_pressed_list + a_key,
                b_directional_pos=(b_x, b_y),
                c_directional_pos=(c_x, c_y),
                d_numeric_pos=(d_x, d_y),
                d_outputs_written=next_d_outputs_written,
                previous_tile=current_tile)
            # print(" " * len(current_tile.a_key_pressed_list), next_tile)
            if next_d_outputs_written == target_d_outputs:
                return next_tile
            if next_tile not in visited_tiles and next_tile not in explore_tiles_to_cost:
                explore_tiles_to_cost.append(next_tile)

output = 0

with open("example_input", "rt") as input_file:
    target_codes = [c.strip() for c in input_file.readlines()]

for target_code in target_codes:
    result = do_search(target_code)
    print(result, len(result.a_key_pressed_list))
    # res_list = [result]
    # while res_list[-1].previous_tile is not None:
    #     res_list.append(res_list[-1].previous_tile)
    #     print("-", res_list[-1])
    # print()

    output += int(target_code.replace("A", "")) * len(result.a_key_pressed_list)

print(output)

def norm(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)


def path_on_pad(from_x, from_y, to_x, to_y, valid_pos) -> Iterable[str]:
    if (from_x, from_y) == (to_x, to_y):
        yield ""
    else:
        for dir, (dir_x, dir_y) in all_directions.items():
            next_x, next_y = from_x + dir_x, from_y + dir_y
            if (next_x, next_y) not in valid_pos:
                continue
            if norm(next_x, next_y, to_x, to_y) < norm(from_x, from_y, to_x, to_y):
                yield from (dir + cont_path for cont_path in path_on_pad(next_x, next_y, to_x, to_y, valid_pos=valid_pos))


def distance(from_vector: str, to_vector: str) -> int:
    """
    Lets assume the vectors look like this:

    from_vector = [A ...... A v x.... ]
    to_vector   = [A ...... A w x.... ]

    :param from_vector:
    :param to_vector:
    :return:
    """
    print("Call:", from_vector, to_vector)
    assert len(from_vector) == len(to_vector)
    dim = len(from_vector)

    if from_vector == to_vector:
        return 0

    leading_a_count = max(i for i in range(dim) if from_vector[:i] == to_vector[:i] == "A" * i)
    assert from_vector[leading_a_count] != to_vector[leading_a_count]
    assert from_vector[leading_a_count + 1:] == to_vector[leading_a_count + 1:]
    common_suffix = from_vector[leading_a_count + 1:]

    if leading_a_count == dim - 1:  # numerical pad.
        pos_to_keys = numeric_key_pad
        keys_to_pos = numeric_keys_to_dir
    else:  # directional pad
        pos_to_keys = directional_key_pad
        keys_to_pos = directional_keys_to_dir

    orig_from_char = from_vector[leading_a_count]
    orig_to_char = to_vector[leading_a_count]
    from_x, from_y = keys_to_pos[orig_from_char]
    to_x, to_y = keys_to_pos[orig_to_char]

    path_distances = {}
    for possible_path in path_on_pad(from_x, from_y, to_x, to_y, valid_pos=pos_to_keys.keys()):
        assert len(possible_path) >= 1
        print("path from", orig_from_char, "to", orig_to_char, "is", possible_path)

        if leading_a_count > 0:
            # if possible path has length 1, then this is like this:
            # from_vector           = [ AAAAAA     A     from_char common_suffix ]   ---> many steps
            # middle_vector         = [ AAAAAA direction from_char common_suffix ]   ---> one step
            # middle_vector_changed = [ AAAAAA direction  to_char  common_suffix ]   ---> many steps
            # to_vector             = [ AAAAAA     A      to_char  common_suffix ]
            #
            # so:
            # distance(from_vector, middle_vector) + 1 + distance(middle_vector_changed, to_vector)

            possible_path_distance = 0

            x, y = from_x, from_y
            intermediate_from = from_vector
            for direction in possible_path:
                from_char = pos_to_keys[(x, y)]
                dir_x, dir_y = all_directions[direction]
                x += dir_x
                y += dir_y
                to_char = pos_to_keys[(x, y)]

                middle_vector         = "A" * (leading_a_count - 1) + direction + from_char + common_suffix
                middle_vector_changed = "A" * (leading_a_count - 1) + direction + to_char   + common_suffix

                possible_path_distance += distance(intermediate_from, middle_vector) + 1
                intermediate_from = middle_vector_changed

            possible_path_distance += distance(intermediate_from, to_vector)
        else:
            # we can just directly navigate the key pad.
            possible_path_distance = len(possible_path)

        path_distances[possible_path] = possible_path_distance

    # take the shortest
    return min(path_distances.values())

def dist_for_code(num_robot_pads, target_code):
    codes = ["A" * num_robot_pads + c for c in "A" + target_code]
    # to go to the next code, and + 1 to actually print it.
    return sum(distance(a, b) + 1 for a, b in zip(codes[:-1], codes[1:]))

# to press 3:
print(dist_for_code(2, "379A"))
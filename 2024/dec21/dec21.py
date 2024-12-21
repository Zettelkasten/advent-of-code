from __future__ import annotations
import dataclasses
import re


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


def do_search(target_d_outputs: str) -> Tile:
    initial_pos = Tile(
        a_key_pressed_list="", b_directional_pos=(2, 0), c_directional_pos=(2, 0),
        d_numeric_pos=(2, 3), d_outputs_written="", previous_tile=None)

    visited_tiles: set[Tile] = set()
    explore_tiles_to_cost: set[Tile] = {initial_pos}

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
            if next_tile not in visited_tiles:
                explore_tiles_to_cost.add(next_tile)

output = 0

with open("input", "rt") as input_file:
    target_codes = [c.strip() for c in input_file.readlines()]

    for target_code in target_codes:
        result = do_search(target_code)
        print(result, len(result.a_key_pressed_list), "*", int(target_code.replace("A", "")))
        # res_list = [result]
        # while res_list[-1].previous_tile is not None:
        #     res_list.append(res_list[-1].previous_tile)
        #     print("-", res_list[-1])
        # break

        output += int(target_code.replace("A", "")) * len(result.a_key_pressed_list)

print(output)
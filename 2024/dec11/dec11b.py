import dataclasses
from collections import defaultdict
from typing import Dict, Tuple, List

with open("input", "rt") as input_file:
    input = [int(val) for val in input_file.read().split()]

# cache the results
@dataclasses.dataclass
class StoneCache:
    stone: int
    num_blinks_to_new_stones: Dict[int, List[int]]

cache: Dict[int, StoneCache] = {}

def blink_once(stone: int) -> List[int]:
    str_stone = str(stone)
    if stone == 0:
        return [1]
    elif len(str_stone) % 2 == 0:
        half_len = len(str_stone) // 2
        return [int(str_stone[:half_len]), int(str_stone[half_len:])]
    else:
        return [stone * 2024]


def process_stones(num_blinks: int, stones: list[int]) -> list[int]:
    if num_blinks == 0:
        return stones
    new_stones = []

    for stone in stones:
        if not stone in cache:
            cache[stone] = StoneCache(stone, {0: [stone]})
        highest_cached_value = max(key for key in cache[stone].num_blinks_to_new_stones.keys() if key <= num_blinks)
        old_value = cache[stone].num_blinks_to_new_stones[highest_cached_value]
        blinks_left = num_blinks - highest_cached_value
        assert blinks_left >= 0, (num_blinks, cache[stone])
        if blinks_left == 0:
            new_stones.extend(old_value)
        else:
            blinked_stones = [new_stone for old_stone in old_value for new_stone in process_stones(blinks_left - 1, blink_once(old_stone))]
            cache[stone].num_blinks_to_new_stones[num_blinks] = blinked_stones
            new_stones.extend(blinked_stones)
    return new_stones

assert process_stones(6, [125, 17]) == [2097446912, 14168, 4048, 2, 0, 2, 4, 40, 48, 2024, 40, 48, 80, 96, 2, 8, 6, 7, 6, 0, 3, 2]
assert process_stones(0, [125, 17]) == [125, 17]
assert process_stones(1, [125, 17]) == [253000, 1, 7]
assert process_stones(2, [125, 17]) == [253, 0, 2024, 14168]
assert process_stones(3, [125, 17]) == [512072, 1, 20, 24, 28676032]

for i in range(1, 75 + 1):
    print(i, len(process_stones(i, input)))

"""

125     17
 |      |  \
253000  1   7

"""

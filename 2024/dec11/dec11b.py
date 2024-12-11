from collections import Counter

with open("input", "rt") as input_file:
    input = Counter([int(val) for val in input_file.read().split()])

for round in range(1, 76):
    next_input = Counter()
    for stone, count in input.items():
        str_stone = str(stone)
        if stone == 0:
            next_input[1] += count
        elif len(str_stone) % 2 == 0:
            half_len = len(str_stone) // 2
            next_input[int(str_stone[:half_len])] += count
            next_input[int(str_stone[half_len:])] += count
        else:
            next_input[stone * 2024] += count
    input = next_input
    print(round, sum(input.values()))

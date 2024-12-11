with open("input", "rt") as input_file:
    input = [int(val) for val in input_file.read().split()]

for round in range(25):
    next_input = []
    for stone in input:
        str_stone = str(stone)
        if stone == 0:
            next_input.append(1)
        elif len(str_stone) % 2 == 0:
            half_len = len(str_stone) // 2
            next_input.append(int(str_stone[:half_len]))
            next_input.append(int(str_stone[half_len:]))
        else:
            next_input.append(stone * 2024)
    print(input)
    input = next_input

print(len(input))
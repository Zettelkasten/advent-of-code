import numpy
lines = open("input").readlines()
out = 0
for line in lines:
    numbers = [int(num) for num in line.strip()]
    nums_to_pick = 12
    last_picked = -1
    picked = []
    for num_pick in range(nums_to_pick):
        pick_from = numbers[last_picked+1:-(nums_to_pick - num_pick - 1)] if num_pick != nums_to_pick - 1 else numbers[last_picked+1:]
        best_pick = numpy.argmax(pick_from) + last_picked + 1
        picked.append(numbers[best_pick])
        last_picked = best_pick
    total_val = int("".join(str(d) for d in picked))
    print(line.strip(), total_val)
    out += total_val
print("b", out)
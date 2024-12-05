first_list, second_list = [], []
with open("input", "rt") as input_file:
    for line in input_file.readlines():
        first_input, second_input = line.split()
        first_list.append(int(first_input))
        second_list.append(int(second_input))

assert len(first_list) == len(second_list)

# part a
print(sum(abs(a - b) for a, b in zip(sorted(first_list), sorted(second_list))))

# part b

def part_b(first_list, second_list):
    first_list = sorted(first_list)
    second_list = sorted(second_list)
    second_list_pointer = 0

    res = 0

    for first_input in first_list:
        # move second pointer ahead in sorted list until we find "first_input"
        while second_list[second_list_pointer] < first_input:
            second_list_pointer += 1
            if second_list_pointer >= len(second_list):
                return res
        # add while the second list matches the first_input
        while second_list[second_list_pointer] == first_input:
            res += first_input
            second_list_pointer += 1
            if second_list_pointer >= len(second_list):
                return res
    return res

print(part_b(first_list, second_list))
left_right_pairs = []
with open("input", "rt") as input_file:
    for line in input_file.readlines():
        left, right = line.split(": ")
        left_right_pairs.append((int(left), [int(r) for r in right.split(" ")]))

def can_do(left, rights):
    if len(rights) == 1:
        return left == rights[0]
    else:
        *rest, last = rights
        if left % last == 0 and can_do(left // last, rest):
            return True
        elif left - last >= 0 and can_do(left - last, rest):
            return True
        elif str(left).endswith(str(last)) and can_do(left // (10 ** len(str(last))), rest):
            return True
        return False

print(can_do(40, [10, 3, 10]))
print(sum(left for left, rights in left_right_pairs if can_do(left, rights)))
import numpy
ranges = [seg.split("-") for seg in open("input").read().split(",")]
out = 0

def check_num(num: int):
    num = numpy.asarray([ord(c) for c in str(num)])
    for num_splits in range(2, len(num) + 1):
        if len(num) % num_splits != 0:
            continue
        splits = num.reshape(num_splits, -1)
        if all((splits[0, :] == splits[i, :]).all() for i in range(1, num_splits)):
            return True
    return False

for left, right in ranges:
    print(left, "-", right)

    for num in range(int(left), int(right) + 1):
        if check_num(num):
            print("  ", num)
            out += num

print("b", out)

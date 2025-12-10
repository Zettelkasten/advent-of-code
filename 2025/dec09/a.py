import math

pairs = [line.strip().split(",") for line in open("input")]
pairs = [(int(x), int(y)) for x, y in pairs]
def area(i, j):
    return (math.fabs(pairs[i][0] - pairs[j][0]) + 1) * (math.fabs(pairs[i][1] - pairs[j][1]) + 1)
print(max(area(i, j) for i in range(len(pairs)) for j in range(len(pairs))))
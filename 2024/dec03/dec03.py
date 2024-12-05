import re

with open("input", "rt") as input_file:
    matches = re.findall(r"mul\((\d+),(\d+)\)", input_file.read())

# part a
print(sum(int(a) * int(b) for a, b in matches))

# part b
with open("input", "rt") as input_file:
    matches = re.findall(r"(do\(\))|(don't\(\))|(mul\((\d+),(\d+)\))", input_file.read())

enabled = True
res = 0
for match in matches:
    print(match)
    do, dont, mul, a, b = match
    if do:
        enabled = True
    elif dont:
        enabled = False
    elif mul and enabled:
        res += int(a) * int(b)
print(res)
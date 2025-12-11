with open("input") as file:
    lines = [line.split(": ") for line in file.readlines()]
    adj = {a: b.split() for a, b in lines}

def count_paths(start):
    if start == "out":
        return 1
    return sum(count_paths(n) for n in adj[start])

print(count_paths("you"))
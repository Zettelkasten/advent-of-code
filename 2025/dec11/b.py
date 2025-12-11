import functools

with open("input") as file:
    lines = [line.split(": ") for line in file.readlines()]
    adj = {a: b.split() for a, b in lines}

@functools.lru_cache(None)
def count_paths(start, goal: str):
    if start == goal:
        return 1
    if start == "out":
        return 0
    return sum(count_paths(n, goal=goal) for n in adj[start])

total = count_paths("svr", "dac") * count_paths("dac", "fft") * count_paths("fft", "out") \
+ count_paths("svr", "fft") * count_paths("fft", "dac") * count_paths("dac", "out")
print(total)
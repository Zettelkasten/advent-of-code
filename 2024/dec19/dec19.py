import re
from collections import defaultdict

with open("input", "rt") as input_file:
    lines = input_file.readlines()

    available_patterns = lines[0].strip().split(", ")
    desired_towels = [line.strip() for line in lines[2:]]


# part a
can_make = re.compile("(" + "|".join(available_patterns) + ")*")
print(sum(1 for towel in desired_towels if can_make.fullmatch(towel)))

# part b
cache = {}

def count_matches(word):
    if word in cache:
        return cache[word]
    if len(word) == 0:
        return 1
    total = 0
    for pattern in available_patterns:
        if word.startswith(pattern):
            total += count_matches(word[len(pattern):])
    cache[word] = total
    return total

print(sum(count_matches(towel) for towel in desired_towels))
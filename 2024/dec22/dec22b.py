from collections import defaultdict, Counter

import numpy as np
from tqdm import tqdm

def next_secret_number(secret):
    secret = ((secret * 64) ^ secret) % 16777216  #
    secret = ((secret // 32) ^ secret) % 16777216
    secret = ((secret * 2048) ^ secret) % 16777216
    return secret


def next_secret_number_v2(secret):
    # 24 bit number
    secret = (secret << 6) ^ secret


res = 0
with open("input", "rt") as input_file:
    initial_numbers = [int(line) for line in input_file.readlines()]

num_to_next = {}

num_collisions = 0

keys_to_profits = Counter()

for num in tqdm(initial_numbers):
    num_sequence = [num]
    for _ in range(2000):
        num_sequence.append(next_secret_number(num_sequence[-1]))
    num_sequence = np.asarray(num_sequence)
    prices_sequence = num_sequence % 10
    price_diff_sequence = prices_sequence[1:] - prices_sequence[:-1]
    assert len(price_diff_sequence) == 2000

    keys_for_this_sequence = set()

    for pos in range(3, 2000 - 1):
        key = tuple(price_diff_sequence[pos - 3:pos + 1])
        if key not in keys_for_this_sequence:
            keys_to_profits[key] += prices_sequence[pos + 1]
            keys_for_this_sequence.add(key)

best_key = max(keys_to_profits, key=keys_to_profits.get)
print(best_key, keys_to_profits[best_key])
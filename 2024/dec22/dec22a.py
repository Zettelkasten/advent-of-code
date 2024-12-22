def next_secret_number(secret):
    secret = ((secret * 64) ^ secret) % 16777216
    secret = ((secret // 32) ^ secret) % 16777216
    secret = ((secret * 2048) ^ secret) % 16777216
    return secret

res = 0
with open("input", "rt") as input_file:
    for line in input_file.readlines():
        num = int(line)
        for _ in range(2000):
            num = next_secret_number(num)
        res += num

print(res)
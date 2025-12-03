ranges = [seg.split("-") for seg in open("input").read().split(",")]
out = 0
for left, right in ranges:
    print(left, "-", right)
    if len(left) % 2 != 0:
        left = "1" + "0" * len(left)
    if len(right) % 2 != 0:
        right = "9" * len(right)
    left_first, left_second = int(left[:len(left) // 2]), int(left[-len(left) // 2:])
    right_first, right_second = int(right[:len(right) // 2]), int(right[-len(right) // 2:])
    left_digit = min(left_first, left_second)
    right_digit = max(right_first, right_second)
    for digit in range(left_digit, right_digit + 1):
        this = int(str(digit) + str(digit))
        if int(left) <= this <= int(right):
            out += this
            print(" ", this)

print("a", out)
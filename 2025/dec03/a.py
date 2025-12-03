import numpy
lines = open("input").readlines()
out = 0
for line in lines:
    numbers = [int(num) for num in line.strip()]
    highest_first = numpy.argmax(numbers[:-1])
    highest_second = numpy.argmax(numbers[highest_first+1:]) + highest_first + 1
    best = numbers[highest_first] * 10 + numbers[highest_second]
    print(line.strip(), best)
    out += best
print("a", out)
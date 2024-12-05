with open("input", "rt") as input_file:
    reports = [[int(val) for val in line.split()] for line in input_file.readlines()]

# part a
def part_a(report):
    diffs = [a - b for a, b in zip(report[1:], report[:-1])]
    min_diff, max_diff = min(diffs), max(diffs)
    return -3 <= min_diff <= max_diff <= -1 or 1 <= min_diff <= max_diff <= 3

print(len(reports))
print(len([1 for report in reports if part_a(report)]))

def part_b(report_):
    for skip in range(len(report_)):
        report = report_[:skip] + report_[skip+1:]
        diffs = [a - b for a, b in zip(report[1:], report[:-1])]
        min_diff, max_diff = min(diffs), max(diffs)
        if -3 <= min_diff <= max_diff <= -1 or 1 <= min_diff <= max_diff <= 3:
            return True
    return False


print(len([1 for report in reports if part_b(report)]))
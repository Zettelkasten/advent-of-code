import dataclasses
import itertools

import numpy


@dataclasses.dataclass
class Line:
    diagram: numpy.ndarray
    buttons: list[numpy.ndarray]

def parse_line(line):
    diagram, *buttons, joltage = line.split()
    diagram = diagram.removeprefix('[').removesuffix(']')
    diagram = numpy.asarray(tuple({"#": 1, ".": 0}[c] for i, c in enumerate(diagram)), dtype=int)
    return Line(
        diagram=diagram,
        buttons=[numpy.asarray(tuple((1 if digit in eval(button.replace(")", ",)")) else 0) for digit in range(len(diagram))), dtype=int) for button in buttons]
    )

lines = [parse_line(line) for line in open("input").readlines()]

total_count = 0
for line in lines:
    found_any = False
    for count in range(1, len(line.diagram)):
        okay = any(numpy.all(numpy.stack(comb, axis=0).sum(axis=0) % 2 == line.diagram) for comb in itertools.combinations(line.buttons, r=count))

        if okay:
            print(count)
            total_count += count
            found_any = True
            break
    if not found_any:
        assert False

print(total_count)
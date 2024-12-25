import dataclasses
import itertools
import unittest
from collections import defaultdict

from networkx.classes import nodes

initial_inputs_from_input = {}

@dataclasses.dataclass()
class Gate:
    x: str
    op: str
    y: str
    res: str

    def __hash__(self):
        return hash((self.x, self.op, self.y, self.res))

input_name_to_gates: dict[str, set[Gate]] = defaultdict(set)
all_gates = {}

with open("input", "rt") as input_file:
    read_gates = False
    for line in input_file.readlines():
        line = line.strip()
        if not read_gates:
            if line == "":
                read_gates = True
            else:
                a, b = line.split(": ")
                initial_inputs_from_input[a] = {"0": False, "1": True}[b]
        else:
            a, b = line.split(" -> ")
            x, op, y = a.split(" ")
            gate = Gate(x=x, op=op, y=y, res=b)
            input_name_to_gates[x].add(gate)
            input_name_to_gates[y].add(gate)
            all_gates[gate.res] = gate


def evaluate(gates: dict[str, Gate], inputs: dict[str, bool], outputs: list[str]):
    def eval_single(name):
        if name in gates:
            gate = gates[name]
            if gate.op == "AND":
                return eval_single(gate.x) and eval_single(gate.y)
            elif gate.op == "OR":
                return eval_single(gate.x) or eval_single(gate.y)
            elif gate.op == "XOR":
                return eval_single(gate.x) != eval_single(gate.y)
            else:
                assert False, gate
        elif name in inputs:
            return inputs[name]
        else:
            assert False, name

    yield from (eval_single(name) for name in outputs)


def bin_to_int(x):
    return sum(int(x) * 2 ** i for i, x in enumerate(x))

def compute_num(x, y, gates):
    assert len(x) == len(y) == 45
    inputs = {**{f"x{i:02}": xx for i, xx in enumerate(x)}, **{f"y{i:02}": yy for i, yy in enumerate(y)}}
    output_names = [f"z{i:02}" for i in range(46)]

    z = f"{bin_to_int(x) + bin_to_int(y):b}"[::-1]
    z += "0" * (46 - len(z))
    expected_output = [{"0": False, "1": True}[digit] for digit in z]

    actual_output = list(evaluate(gates, inputs, output_names))
    print(actual_output)
    print(expected_output)
    return all(a == b for a, b in itertools.zip_longest(actual_output, expected_output))

swap_list = []

def swap_gates(a, b):
    # all_gates[a].op = all_gates[a].op + "*"
    # all_gates[b].op = all_gates[b].op + "*"

    all_gates[a].res, all_gates[b].res = all_gates[b].res, all_gates[a].res
    all_gates[a], all_gates[b] = all_gates[b], all_gates[a]
    swap_list.extend([a, b])


swap_gates("hcm", "gfv")  # to fix z36
swap_gates("z11", "tqm")  # to fix z11
swap_gates("z06", "vwr")  # to fix z06
swap_gates("z16", "kfs")  # to fix z16
print(",".join(sorted(swap_list)))

class Test(unittest.TestCase):

    def check_node(self, z_gate: Gate):
        assert z_gate.op == "XOR"
        in_a, in_b = all_gates[z_gate.x], all_gates[z_gate.y]
        assert {in_a.op, in_b.op} == {"XOR", "OR"}
        in_xor = in_a if in_a.op == "XOR" else in_b
        in_or = in_a if in_a.op == "OR" else in_b

        assert {in_xor.x, in_xor.y} == {"x" + z_gate.res[1:], "y" + z_gate.res[1:]}


    def test_all(self):
        for node in [f"z{i:02}" for i in range(46)]:
            with self.subTest(f"Test {node}"):
                self.check_node(all_gates[node])


from graphviz import Digraph

dot = Digraph()
for i in initial_inputs_from_input:
    dot.node(i, i)
for node in all_gates.values():
    dot.node(node.res, node.res + "=" + node.op)

dot.edges([(node.x, node.res) for node in all_gates.values()] + [(node.y, node.res) for node in all_gates.values()])

print(dot.source)
dot.render(view=True, filename="swapped")

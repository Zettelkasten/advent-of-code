import dataclasses
from collections import defaultdict

initial_inputs = {}

@dataclasses.dataclass(frozen=True)
class Gate:
    x: str
    op: str
    y: str
    res: str

    def __hash__(self):
        return hash((self.x, self.op, self.y, self.res))

input_name_to_gates: dict[str, set[Gate]] = defaultdict(set)
all_gates = []

with open("input", "rt") as input_file:
    read_gates = False
    for line in input_file.readlines():
        line = line.strip()
        if not read_gates:
            if line == "":
                read_gates = True
            else:
                a, b = line.split(": ")
                initial_inputs[a] = {"0": False, "1": True}[b]
        else:
            a, b = line.split(" -> ")
            x, op, y = a.split(" ")
            gate = Gate(x=x, op=op, y=y, res=b)
            input_name_to_gates[x].add(gate)
            input_name_to_gates[y].add(gate)
            all_gates.append(gate)

computed_outputs = {}


def update_input(input_name, val: bool):
    print(input_name, ':=', val, input_name_to_gates[initial_input_name])
    computed_outputs[input_name] = val
    for gate in list(input_name_to_gates[input_name]):
        if gate.res in computed_outputs:
            continue  # already evaluated
        if gate.x in computed_outputs and gate.y in computed_outputs:
            # can eval
            if gate.op == "AND":
                res = computed_outputs[gate.x] and computed_outputs[gate.y]
            elif gate.op == "OR":
                res = computed_outputs[gate.x] or computed_outputs[gate.y]
            elif gate.op == "XOR":
                res = computed_outputs[gate.x] != computed_outputs[gate.y]
            else:
                assert False, gate
            update_input(gate.res, res)


for initial_input_name, val in initial_inputs.items():
    update_input(initial_input_name, val)

output_names = [res_name for res_name in sorted(computed_outputs) if res_name.startswith("z")]
print(sum(int(computed_outputs[res_name]) * 2 ** i for i, res_name in enumerate(output_names)))
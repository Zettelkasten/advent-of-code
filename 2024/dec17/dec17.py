import itertools
from itertools import zip_longest

from tqdm import tqdm

with open("input", "rt") as input_file:
    lines = input_file.readlines()
    assert lines[0].startswith("Register A: ")
    assert lines[1].startswith("Register B: ")
    assert lines[2].startswith("Register C: ")
    assert lines[4].startswith("Program: ")
    reg_a = int(lines[0].split(": ")[1])
    reg_b = int(lines[1].split(": ")[1])
    reg_c = int(lines[2].split(": ")[1])
    program = [int(a) for a in lines[4].split(": ")[1].strip().split(",")]

def simulate(program, reg_a, reg_b, reg_c):
    instr_ptr = 0
    while instr_ptr < len(program):
        lit = program[instr_ptr + 1]
        comb = program[instr_ptr + 1]
        if comb == 4:
            comb = reg_a
        elif comb == 5:
            comb = reg_b
        elif comb == 6:
            comb = reg_c
        elif comb == 7:
            assert False, comb

        if program[instr_ptr] == 0:  # adv
            num = reg_a
            den = 2 ** comb
            reg_a = num // den
        elif program[instr_ptr] == 1:  # bxl
            reg_b = reg_b ^ lit
        elif program[instr_ptr] == 2:  # bst
            reg_b = comb % 8
        elif program[instr_ptr] == 3:  # jnz
            if reg_a != 0:
                instr_ptr = lit
                continue
        elif program[instr_ptr] == 4:  # bxc
            reg_b = reg_b ^ reg_c
        elif program[instr_ptr] == 5:  # out
            yield comb % 8
        elif program[instr_ptr] == 6:  # bdv
            num = reg_a
            den = 2 ** comb
            reg_b = num // den
        elif program[instr_ptr] == 7:  # cdv
            num = reg_a
            den = 2 ** comb
            reg_c = num // den

        instr_ptr += 2

print("part a:")
print(",".join(str(a) for a in simulate(program, reg_a, reg_b, reg_c)))

def make_input_from_seq(program):
    val = 0
    for i, a in enumerate(program):
        val += a * (8 ** i)
    return val

orig_program = program.copy()

print("Desired output", orig_program)

def try_all(length_tried, program):
    if length_tried == len(program):
        print("Correct", program, make_input_from_seq(program))
        exit()

    for i in range(8):
        program[-(length_tried + 1)] = i
        sim = list(simulate(orig_program, make_input_from_seq(program), reg_b, reg_c))
        print(" " * length_tried, program, "gives", sim)
        if sim[-(length_tried + 1):] == orig_program[-(length_tried + 1):]:
            print(" " * length_tried, "Good!")
            try_all(length_tried + 1, program)

try_all(0, [3] * len(orig_program))
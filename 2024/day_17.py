import re
from typing import Dict, List
from math import floor

def get_combo_operand(operand: int, registers: Dict[str, int]):
    if operand < 4:
        return operand
    elif operand==4:
        return registers["A"]
    elif operand==5:
        return registers["B"]
    elif operand==6:
        return registers["C"]


def execute_program(program: List[int], registers: Dict[str, int]):
    instruction_pointer = 0
    output_str = ""
    while instruction_pointer < len(program):
        instruction = program[instruction_pointer]
        literal_operand = program[instruction_pointer+1]
        # print(instruction, literal_operand)
        combo_operand = get_combo_operand(literal_operand, registers)
        if instruction==0:
            registers["A"] = floor(registers["A"]/(2**combo_operand))
        elif instruction==6:
            registers["B"] = floor(registers["A"]/(2**combo_operand))
        elif instruction==7:
            registers["C"] = floor(registers["A"]/(2**combo_operand))
        elif instruction == 1:
            registers["B"] = registers["B"] ^ literal_operand
        elif instruction == 3:
            if registers["A"] != 0:        
                instruction_pointer = literal_operand
                continue
        elif instruction == 4:
            registers["B"] = registers["B"] ^ registers["C"]
        elif instruction == 5:
            output_str += f"{combo_operand % 8},"
        elif instruction == 2:
            registers["B"] = combo_operand % 8
            # set the instruction pointer
        instruction_pointer+=2
    if ',' in output_str:
        output_str = output_str[0:-1]
    return output_str, registers

def execute_with_a(program, A):
    return execute_program(program,{"A":A,"B":0,"C":0})


input_file = "2024/inputs/day_17_input.txt"
# input_file = "2024/inputs/day_17_example.txt"
# input_file = "2024/inputs/day_17_example_2.txt"

input_re = r"Register ([A-Z]): (\d+)"

registers = {}
with open(input_file,'r') as f_in:
    for line in f_in:
        matching = re.match(input_re, line)
        if matching:
            registers[matching.groups()[0]] = int(matching.groups()[1])
        if "Program" in line:
            program = [int(x) for x in line.split()[1].split(',')]

print(f"The answer to part 1 is {execute_program(program, registers)[0]}")

triads = [[0,0,0],[0,0,1],[0,1,0],[0,1,1],
          [1,0,0],[1,0,1],[1,1,0],[1,1,1]]

binary = [1 for _ in range(48)]

b_to_try = [binary]
for j in range(0,16):
    next_level = []
    for b in b_to_try:
        target_digit = str(program[15-j])
        i_low = 3*j
        i_high = 3*(j+1)
        for triad in triads:
            if j == 0 and triad[0]==0:
                continue
            b[i_low:i_high] = triad
            A = int("".join([str(x) for x in b]),2)
            output = execute_with_a(program, A)[0].replace(',','')
            if output[15-j] == target_digit:
                next_level.append([x for x in b])
    b_to_try = next_level

As = []
for b in b_to_try:
    A = int("".join([str(x) for x in b]),2)
    As.append(A)
    assert execute_with_a(program,A)[0]==",".join([str(x) for x in program])

print(f"The answer to part 2 is {min(As)}")

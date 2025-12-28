from typing import Iterable
from math import floor
test_input = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""
def sign(number):
    if number < 0:
        return -1
    return 1

def parse_input(input: Iterable):
    output = []
    for line in input:
        # print(line)
        direction = line[0]
        number = int(line[1:])
        output.append(number if direction == "R" else -number)
    return output

file_in = "2025/data_1.txt"
input = open(file_in)
dial_pos = 50
on_zero = 0
for number in parse_input(input):
# for number in parse_input(test_input.split()):
    dial_pos = (dial_pos + number) % 100
    if dial_pos == 0:
        on_zero += 1
print(f"The answer to part 1 is {on_zero}")

input = open(file_in)
dial_pos = 50
on_zero = 0
for number in parse_input(input):
# for number in parse_input(test_input.split()):
    rotations = abs(number) // 100
    remainder = number - (sign(number)*(abs(number)//100))*100
    if dial_pos>0 and ((dial_pos + remainder)>=100 or (dial_pos+remainder)<=0):
        rotations+=1 

    dial_pos = (dial_pos + number) % 100
    on_zero += rotations
print(f"The answer to part 2 is {on_zero}")

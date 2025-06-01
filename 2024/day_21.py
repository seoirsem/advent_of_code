from typing import List
from math import copysign
from functools import cache

def x_seq(dx):
    sequence = ""
    for _ in range(abs(dx)):
        if copysign(1,dx) == 1:
            sequence+=">"
        else:
            sequence+="<"
    return sequence

def y_seq(dy):
    sequence = ""
    for _ in range(abs(dy)):
        if copysign(1,dy) == 1:
            sequence+="v"
        else:
            sequence+="^"
    return sequence

# @cache
def pass_gap_x(char1, dx, pad):
    for line in pad:
        if char1 in line:
            if '.' not in line:
                return False
            if line.index(char1) + dx == line.index('.'):
                return True
    else:
        return False
    
# @cache
def pass_gap_y(char1, dy, pad):
    for i, line in enumerate(pad):
        if char1 in line:
            idx_char = line.index(char1)
            i_char = i
        if '.' in line:
            idx_gap = line.index('.')
            i_gap = i
    if i_gap+dy == i_char and idx_gap==idx_char:
        return True
    else:
        return False

@cache
def pad_travel(char1: str, char2: str, pad: str):
    if pad=="num":
        pad = ["789", "456", "123", ".0A"]
    else:
        pad = [".^A", "<v>"]

    if char1 == char2:
        return ""
    for y, line in enumerate(pad):
        for x, char in enumerate(line):
            if char==char1:
                x1, y1 =x, y
            if char==char2:
                x2, y2 =x, y
    dx = x2-x1
    dy = y2-y1

    # check if we pass the gaps
    # then, if we need to go left, do leri + updo
    # else, do updo + leri
    sequence = ""
    pgx = pass_gap_x(char1,dx, pad)
    pgy = pass_gap_y(char1, dy, pad)
    if pgx or pgy:
        if pgx:
            sequence+=y_seq(dy)
            sequence+=x_seq(dx)
        else:
            sequence+=x_seq(dx)
            sequence+=y_seq(dy)
    elif dx < 0:
        sequence+=x_seq(dx)
        sequence+=y_seq(dy)
    else:
        sequence+=y_seq(dy)
        sequence+=x_seq(dx)

    return sequence

# @cache
def get_len_to_ground(start_char: str, pressed_char: str, this_level: int):
    # print(start_char, pressed_char_char, this_level)
    if this_level == 0: # human controlled pad
        return 1
    else:
        len_out = 0
        initial = "A"
        # print(start_char, pressed_char)
        print(pad_travel(start_char, pressed_char, "arrows")+"A", this_level)

        for c in pad_travel(start_char, pressed_char, "arrows") + "A":
            len_out += get_len_to_ground(initial,c,this_level-1)
            initial= c

        return len_out

def get_sequence(seq_in, initial_state, this_pad):
    seq=""
    for c in seq_in:
        seq += pad_travel(initial_state,c, this_pad) + "A"
        initial_state=c
    return seq

input_file = "2024/inputs/day_21_example.txt"
# input_file = "2024/inputs/day_21_input.txt"

commands = {}
with open(input_file, 'r') as f_in:
    for line in f_in:
        c_num = int(line.rstrip().replace("A",""))
        commands[c_num] = line.rstrip()

complexity = 0
for key, code in commands.items():
    full_s = get_sequence(code, "A", "num")
    r1 = get_sequence(full_s,"A","arrows")
    r2 = get_sequence(r1, "A", "arrows")
    print(len(r2))
    complexity+=key*len(r2)

print(f"The answer to part 1 is {complexity}")

complexity = 0
for key, code in commands.items():
    total_len = 0
    last_char = "A"
    print(get_sequence(code, "A", "num"))
    for c in get_sequence(code, "A", "num"):
        total_len += get_len_to_ground(last_char, c, 2) # go from start to next, then press A
        # print(c, total_len)
        last_char2 = c
    print(key, total_len)
    complexity+=key*total_len

print(f"The answer to part 2 is {complexity}")
# v<<A^>>AAv<A<A^>>AAvAA^<A>A
# v<<AA>A^>AAvA^<A>AAvA^A
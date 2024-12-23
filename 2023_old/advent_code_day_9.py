import re
from functools import cache

filename = "test_input_day_9.txt"
filename = "input_day_9.txt"

value_lists = []
with open(filename, "r") as file:
    for line in file:
        value_lists.append([int(x) for x in line.split()])


def get_next_value(values: list[int])-> int:
    differences = [v2-v1 for v2, v1 in zip(values[1:],values[:-1])]
    if len(differences) == 1:
        return 0
    else:
       return values[-1] + get_next_value(differences)


def get_prev_value(values: list[int])-> int:
    differences = [v2-v1 for v2, v1 in zip(values[1:],values[:-1])]
    if len(differences) == 1:
        return 0
    else:
       return values[0] - get_prev_value(differences)

return_sum = 0
return_2 = 0
for l in value_lists:
    return_sum += get_next_value(l)
    return_2 += get_prev_value(l)
#    return_2 += get_next_value(l[::-1])
print(f"P1: The sum of next values is {return_sum}")
print(f"P2: The sum of previous values is {return_2}")



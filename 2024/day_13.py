import re

eps = 1e-6
COST_A = 3
COST_B = 1
unit_conversion_error = 10000000000000

def claw_game(a_x, a_y, b_x, b_y, t_x, t_y):
    p_a = (t_x*b_y - t_y*b_x)/(b_y*a_x-a_y*b_x)
    p_b = (t_x*a_y - t_y*a_x)/(a_y*b_x-b_y*a_x)
    if (p_a-round(p_a)) < eps and (p_a-round(p_a)) > -eps \
        and (p_b-round(p_b)) < eps and (p_b-round(p_b)) > -eps:
        return round(p_a), round(p_b)

button_re = r"Button .: X\+(\d+), Y\+(\d+)"
target_re = r"Prize: X=(\d+), Y=(\d+)"

input_file = "inputs/day_13_example.txt"
input_file = "inputs/day_13_input.txt"

total_cost = 0
total_cost_2 = 0
with open(input_file, 'r') as input:
    for line in input:
        button_a = re.match(button_re, line.rstrip())
        if button_a is None:
            continue
        button_b = re.match(button_re, next(input).rstrip())
        target = re.match(target_re, next(input).rstrip())
        cost = claw_game(
            *[int(x) for x in button_a.groups()],
            *[int(x) for x in button_b.groups()],
            *[int(x) for x in target.groups()]
        )
        cost2 = claw_game(
            *[int(x) for x in button_a.groups()],
            *[int(x) for x in button_b.groups()],
            *[int(x)+unit_conversion_error for x in target.groups()]
        )

        if cost:
            p_a, p_b = cost
            total_cost += COST_A*p_a + COST_B*p_b
        if cost2:
            p_a, p_b = cost2
            total_cost_2 += COST_A*p_a + COST_B*p_b

print(f"The answer to part 1 is {total_cost}")
print(f"The answer to part 1 is {total_cost_2}")
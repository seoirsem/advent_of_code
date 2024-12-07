from collections import defaultdict


input_file = "day_5_input.txt"
# input_file = "day_5_example.txt"

rules = defaultdict(list)
numberings = []
with open(input_file,'r') as input:
    for line in input:
        if "|" in line:
            a, b = line.rstrip().split("|")
            rules[a].append(b)
        elif "," in line:
            numberings.append(line.rstrip().split(","))

def is_order_good(order, rules):
    for idx, e in enumerate(order):
        if e in rules:
            before = set(order[:idx])
            rules_set = set(rules[e])
            if len(before.intersection(rules_set))>0:
                return False
    return True

incorrect = []
sum_good = 0
for numbering in numberings:
    is_good = is_order_good(numbering, rules)
    if is_good:
        if len(numbering) %2 != 1:
            raise ValueError
        mid_idx = (len(numbering)-1)//2 
        sum_good+=int(numbering[mid_idx])
    else:
        incorrect.append(numbering)

print(f"The answer to part 1 is {sum_good}")        

while_limit = 10

mid_sum = 0
for numbering in incorrect:
    while_count = 0
    is_good = False
    while is_good == False:
        while_count+=1
        if while_count>= while_limit:
            raise ValueError
        for idx, e in enumerate(numbering):
            if e in rules:
                before = numbering[:idx]
                for other in rules[e]:
                    if other in before: # a form of bubble sort, assuming the rules have no cycles
                        idx_other = numbering.index(other)
                        numbering[idx_other] = e
                        numbering[idx] = other
                        break
        is_good = is_order_good(numbering,rules)
    mid_idx = (len(numbering)-1)//2 
    mid_sum+=int(numbering[mid_idx])


print(f"The answer to part 2 is {mid_sum}")
from collections import defaultdict


input_file = "day_5_input.txt"
input_file = "day_5_example.txt"

rules = defaultdict(list)
numberings = []
with open(input_file,'r') as input:
    for line in input:
        if "|" in line:
            a, b = line.rstrip().split("|")
            rules[a].append(b)
        elif "," in line:
            numberings.append(line.rstrip().split(","))


incorrect = []
sum_good = 0
for numbering in numberings:
    is_good = True
    for idx, e in enumerate(numbering):
        if e in rules:
            before = set(numbering[:idx])
            rules_set = set(rules[e])
            if len(before.intersection(rules_set))>0:
                is_good = False
    if is_good:
        if len(numbering) %2 != 1:
            raise ValueError
        mid_idx = (len(numbering)-1)//2 
        sum_good+=int(numbering[mid_idx])
    else:
        incorrect.append(numbering)

print(f"The answer to part 1 is {sum_good}")        


print(incorrect)
for numbering in incorrect:
    is_good = True
    for idx, e in enumerate(numbering):
        if e in rules:
            sorted(key=)
            before = set(numbering[:idx])
            rules_set = set(rules[e])
            overlap = before.intersection(rules_set)
            is_good = False
    if is_good:
        if len(numbering) %2 != 1:
            raise ValueError
        mid_idx = (len(numbering)-1)//2 
        sum_good+=int(numbering[mid_idx])

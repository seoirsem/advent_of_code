from collections import Counter

class Sequence():
    def __init__(self):
        self.elements = [None,None,None,None]
    
    def add_element(self, element):
        self.elements.append(element)
        self.elements = self.elements[1:]
        return self.elements
    
    def hash_val(self):
        return str(self.elements)

    def __eq__(self, other):
        if self.elements == other.elements:
            return True
        return False
    
    def __repr__(self):
        if None in self.elements:
            return "None"
        return f"({",".join([str(x) for x in self.elements])})"
        
def result_after_n(initial: int, n: int):
    for _ in range(n):
        initial = (initial ^ initial*64) % 16777216
        initial = (initial ^ (initial//32)) % 16777216 #2^24
        initial = (initial ^ initial*2048) % 16777216
    return initial

def next_result(this_result: int):
    initial = (this_result ^ this_result*64) % 16777216
    initial = (initial ^ (initial//32)) % 16777216
    return (initial ^ initial*2048) % 16777216

def price(result: int):
    return int(str(result)[-1])

sample = False
if sample:
    number_list = [1,10,100,2024]
else:
    with open(r"2024\inputs\day_22_input.txt", 'r') as input:
        number_list = []
        for line in input:
            number_list.append(int(line.rstrip()))

sec_sum = 0
for line in number_list:
    sec_sum+=result_after_n(int(line), 2000)
        
print(f"The answer to part 1 is {sec_sum}")

if sample:
    number_list = [1,2,3,2024]

seq_seen = Counter()
n_max = 2001
monk_dicts = []
for number in number_list:
    delta, last_cost = None, None
    monk_map = {}
    seq = Sequence()
    for idx in range(n_max+1):
        cost = price(number)
        delta = (cost - last_cost) if last_cost is not None else None
        seq.add_element(delta)
        last_cost = cost

        if idx>3:
            if seq.hash_val() not in monk_map:
                seq_seen[seq.hash_val()] += 1
                monk_map[seq.hash_val()] = cost
        number = next_result(number)
    monk_dicts.append(monk_map)

print("searching for max...")
max_price = 0
max_seq = ""
sums = []
for x in seq_seen:
    
    n_seen = seq_seen[x]
    if n_seen*9 <= max_price: # no way this improves the price
        continue

    price_sum = 0
    for d in monk_dicts:
        if x in d:
            price_sum += d[x]
    
    if price_sum > max_price:
        max_price = price_sum
        max_seq = x

print(f"The answer to part 2 is {max_price}")
print(f"The best sequence is {max_seq}")





import re
from math import lcm

filename = "input_day_8.txt"

def hash_mapping(input: str)-> int:
    numbers = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(i) for i in input]
    hash_sum = 0
    for i, n in enumerate(numbers):
        hash_sum += (27**i)*n
    return hash_sum

location_maps = []
with open(filename, "r") as file:
    instructions = ["LR".index(i) for i in re.sub(r"\s+", "", next(file))] # instructions as 0 (L) or 1 (R)
    for line in file:
        if re.search(r"=", line) != None:
            location_maps.append(re.findall(r"[A-Z]+",line))

hash_map = {}
for ins in location_maps:
    hash_map[hash_mapping(ins[0])] = (hash_mapping(ins[1]), hash_mapping(ins[2]))

location = hash_mapping("AAA")
goal = hash_mapping("ZZZ")
steps = 0
while location != goal:  
    for instruction in instructions:
#        print(location)
        location = hash_map[location][instruction]
        steps += 1
        if location == goal:
            break
print(f"P1: It took {steps} steps to reach the goal")

###########

filename = "test_input_day_8_part_2.txt"
filename = "input_day_8.txt"
location_maps = []
with open(filename, "r") as file:
    instructions = ["LR".index(i) for i in re.sub(r"\s+", "", next(file))] # instructions as 0 (L) or 1 (R)
    for line in file:
        if re.search(r"=", line) != None:
            location_maps.append(re.findall(r"[A-Z]+",line))

hash_map = {}
for ins in location_maps:
    hash_map[ins[0]] = (ins[1],ins[2])


def test_end_in_A(node: str)-> bool:
    if node[2] == "A":
        return True
    else:
        return False
    
def test_end_in_Z(node: str)-> bool:
    if node[2] == "Z":
        return True
    else:
        return False
    
def find_cycle_length(start_node: int, instructions: list[int], hash_map: dict[int,(int,int)])-> (int, int, int):
    visited = {}
    steps = 0
    start_cycle = 0
    cycle_count = 0
    first_z = -1

    visited_bool = False
    visited[start_node] = 0
    print(start_node)
    while True:
        for instruction in instructions:
            start_node = hash_map[start_node][instruction]
            if test_end_in_Z(start_node) and first_z == -1:
                print(start_node)
                first_z = steps
                visited_bool = True
                break
            steps+=1
            if start_node in visited:
                #visited_bool = True
                start_cycle = visited[start_node]
                cycle_count = steps - start_cycle
                #break
            visited[start_node] = steps
        if visited_bool:
            break
    return start_cycle, first_z, cycle_count

    
start_nodes = []
for node in hash_map:
    if test_end_in_A(node):
        start_nodes.append(node)

first_zs = []
cycle_lens = []
for node in start_nodes:
    start_cycle, first_z, cycle_count = find_cycle_length(node,instructions,hash_map)
    print(start_cycle, first_z, cycle_count)
    first_zs.append(first_z)
    cycle_lens.append(cycle_count)


print(lcm(*first_zs))
# steps = 0
# while True:
#     for instruction in instructions:
#         all_end_z = True
#         #print(start_nodes, instruction)
#         for i, node in enumerate(start_nodes):
#             start_nodes[i] = hash_map[node][instruction]
#             #print(hash_map[node][instruction])
#             if not test_end_in_Z(node):
#                 all_end_z = False
#         if all_end_z:
#             break
#         steps += 1

#     if all_end_z:
#         break

print(len(instructions))
print(f"P2: It took {steps} steps to reach the goal")

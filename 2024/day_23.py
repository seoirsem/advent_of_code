from collections import defaultdict
from typing import Dict

file_in = "2024/inputs/day_23_example.txt"
file_in = "2024/inputs/day_23_input.txt"

nodes = defaultdict(set) # node: set

with open(file_in, 'r') as lines:
    for line in lines:
        node_pair = line.rstrip().split('-')
        nodes[node_pair[0]].add(node_pair[1])
        nodes[node_pair[1]].add(node_pair[0])

seen_inv = set()
triples = []
for node1 in nodes.keys():
    if node1[0] != "t":
        continue
    for node2 in nodes[node1]:
        for node3 in nodes[node2]:
            if (node1, node2, node3) in seen_inv or (node1, node3, node2) in seen_inv or \
            (node2, node1, node3) in seen_inv or (node2, node3, node1) in seen_inv or \
            (node3, node2, node1) in seen_inv or (node3, node1, node2) in seen_inv:
                continue
            if node3 in nodes[node1]:
                triples.append((node1, node2, node3))
            seen_inv.add((node1,node2, node3))

print(f"The answer to part 1 is {len(triples)}")

max_set_size = 0
max_set = set()
first_pair_seen = set()

def search_all_connected(node, list_seen, nodes: Dict[str,set], directed_visited):
    node_key = list_seen.copy()
    node_key.append(node)
    node_key.sort()
    node_key = "".join(node_key)
    if node_key in directed_visited:
        return []
    longest_list = []
    for node1 in nodes[node]:
        seen_all = True
        for seen in list_seen:
            if seen not in nodes[node1]:
                seen_all = False
                break
        if seen_all:
            new_list_seen = list_seen.copy()
            new_list_seen.append(node)
            longer_list = search_all_connected(node1, new_list_seen, nodes, directed_visited)            
            if len(longer_list) >= len(longest_list):
                longest_list = longer_list
    longest_list.append(node)
    directed_visited.add(node_key)
    return longest_list

directed_visited = set() # sort alphabetically then concatonate
longest_set = []
for idx, node in enumerate(nodes):
    if (idx+1) % 20 == 0:
        print(f"[{idx+1}]/{len(nodes)}")
    largest_fully_connected = search_all_connected(node, [], nodes, directed_visited)
    if len(largest_fully_connected) > len(longest_set):
        longest_set = largest_fully_connected

longest_set.sort()
print(f"The answer to part 2 is {",".join(longest_set)}")

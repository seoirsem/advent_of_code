from collections import defaultdict
import time

def hash_str(i1, i2):
    list1 = sorted([i1, i2])
    return (list1[0], list1[1])

def perform_operation(operation, x1, x2):
    if operation == "AND":
        return x1 & x2
    elif operation == "XOR":
        return x1 ^ x2
    elif operation == "OR":
        return x1 | x2
    
def node_values_to_int(node_values, letter):
    value_list = []
    for node_value in node_values:
        if node_value[0] == letter:
            value_list.append(node_value)
    keys = sorted(value_list, reverse=True)
    n_str = ""
    for k in keys:
        n_str += str(node_values[k])
    return int(n_str, 2)


input_file = "2024/inputs/daY_24_example2.txt"
input_file = "2024/inputs/daY_24_example.txt"
input_file = "2024/inputs/daY_24_input.txt"

node_values = {}
node_links = defaultdict(set)
operations = defaultdict(list)
with open(input_file,'r') as f:
    for line in f:
        if line == "\n":
            break
        
        node, value = line.strip().split()
        node = node.replace(':', '')
        node_values[node] = int(value)
    for line in f:
        i1, op, i2, _, o = line.strip().split()
        comb_str = hash_str(i1, i2)
        operations[comb_str].append((op, o))
        node_links[i1].add(i2)
        node_links[i2].add(i1)

def load_data(val_strs, op_strs):


def compute(nv, ops, nls):
    node_links = nls.copy()
    node_values = nv.copy()
    operations = ops.copy()
    z_values = {}
    while len(operations) > 0:
        new_values = []
        removed_values = []
        for node, value in node_values.items():
            if node[0] == 'z':
                z_values[node] = value
            completed_other = []
            for node_link in node_links[node]:
                if node_link in node_values:
                    value2 = node_values[node_link]
                else:
                    continue
                completed = []
                for op, result_node in operations[hash_str(node, node_link)]:
                    new_values.append((result_node,perform_operation(op, value, value2)))
                completed_other.append(node_link)

            for completed in completed_other:
                node_links[node].remove(completed)
                node_links[completed].remove(node)
                operations.pop(hash_str(completed, node))
                if len(node_links[completed]) == 0:
                    removed_values.append(completed)
                if len(node_links[node]) == 0:
                    removed_values.append(node)
        for node, value in new_values:
            node_values[node] = value
            if node[0] == 'z':
                z_values[node] = value
        for node in removed_values:
            if node[0] == "z":
                z_values[node] = node_values[node]
            if node in node_values:
                node_values.pop(node)
    keys = sorted(list(z_values.keys()), reverse=True)
    n_str = ""
    for k in keys:
        n_str += str(z_values[k])
    return n_str

tstart = time.time()
for _ in range (1):
    v = int(compute(node_values, operations, node_links),2)
print(f"time: {time.time() - tstart:.4f}")
print(len(operations), v)
print(f"The answer to part 1 is {int(compute(node_values, operations, node_links),2)}")


x = node_values_to_int(node_values, 'x')
y = node_values_to_int(node_values, 'y')

print(x, y, x+y)


test_ops = operations.copy()

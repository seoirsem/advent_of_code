from typing import Optional, Union, List
import time

class Node():
    def __init__(self, value: int, left: Optional["Node"], right: Optional["Node"]):
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return f"Node: {self.value}"
    
    def split_self(self, left_val: int, right_val: int):
        outer_right = self.right
        right_node = Node(right_val, self, outer_right)
        self.right = right_node
        self.value = left_val
        return outer_right

def transform(number: int) -> Union[List[int], int]:
    num_str = str(number)
    if number == 0:
        return 1
    elif len(num_str) % 2 == 0:
        mid_pt = len(num_str)//2
        return [int(num_str[0:mid_pt]), int(num_str[mid_pt:])]
    else:
        return number * 2024

def queue_to_list(start_node: Node)-> list[int]:
    list_out = []
    this_node = start_node
    while this_node is not None:
        list_out.append(this_node.value)
        this_node = this_node.right
    return list_out

def list_to_queue(list_in: List[int]) -> Node:
    head_node = Node(list_in[0], None, None)
    prev_node = head_node
    for x in list_in[1:]:
        prev_node.right = Node(x, prev_node, None)
        prev_node = prev_node.right
    return head_node

def blink_transform(head_node: Node)->Node:
    this_node = head_node
    prev_node = None
    while this_node is not None:
        prev_node = this_node
        transformed_val = transform(this_node.value)
        if type(transformed_val) is int:
            this_node.value = transformed_val
            this_node = this_node.right
        else:
            if this_node.right is None:
                this_node.split_self(transformed_val[0], transformed_val[1])
                break
            else:
                this_node = this_node.split_self(transformed_val[0], transformed_val[1])
    return prev_node

def linked_list_length(head_node: Node)-> int:
    this_node = head_node
    count = 0
    while this_node is not None:
        count+=1
        this_node = this_node.right
    return count

day_11_input = [70949, 6183, 4, 3825336, 613971, 0, 15, 182]
# day_11_input = [125, 17] #example

start_time = time.time()
head_node = list_to_queue(day_11_input)
for _ in range(25):
    blink_transform(head_node)
print(f"Time taken: {time.time() - start_time:.3f}")
print(f"The answer to part 1 is {linked_list_length(head_node)}")


def recursive_stone_search(stone_number: int, stone_map, target_depth: int)-> int:
    if target_depth == 0:
        return 1
    if (stone_number, target_depth) in stone_map:
        return stone_map[(stone_number, target_depth)]
    transformed = transform(stone_number)
    if type(transformed) is int:
        val_out = recursive_stone_search(transformed, stone_map, target_depth-1)
    else: 
        val_out = recursive_stone_search(transformed[0], stone_map, target_depth-1) + recursive_stone_search(transformed[1], stone_map, target_depth-1)
    stone_map[(stone_number, target_depth)] = val_out
    return val_out

stone_map = {} # (start_stone_num, number_blinks): number_stones
target = 75
start_time = time.time()
total_count = 0
for x in day_11_input:
    total_count+=recursive_stone_search(x, stone_map, target)

print(f"Time taken: {time.time() - start_time:.3f}")
print(f"The answer to part 2 is {total_count}")

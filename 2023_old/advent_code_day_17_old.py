import re
import heapq

# a preferred q of all paths, starting with minimal heat

filename = "test_input_day_17.txt"
#filename = "input_day_17.txt"
arr = []
with open(filename,"r") as file:
    for line in file:
        arr.append([int(x) for x in line.replace("\n","")])

WIDTH = len(arr[0])
HEIGHT = len(arr)
# for each path, we go: [total_heat_cost, (pos-1), (pos_-2), (pos_-3)]

def calculate_allowable_directions(path: list)-> list:
    #U,D,L,R based on sides of box and previous travel
    directions = []
    dir = (path[1][0] - path[2][0], path[1][1] - path[2][1])
    dir2 = (path[2][0] - path[3][0],path[2][1] - path[3][1])
    dir3 = (path[3][0] - path[4][0],path[3][1] - path[4][1])
    if dir[0] == 1 or dir[0] == -1:
        directions.append((0,1))
        directions.append((0,-1))
        if dir != dir2 and dir2 != dir3: # same direction for 3 tiles
            directions.append(dir) # can still go forward
    if dir[1] == 1 or dir[1] == -1:
        directions.append((1,0))
        directions.append((-1,0))
        if dir != dir2 and dir2 != dir3: # same direction for 3 tiles
            directions.append(dir) # can still go forward

    return directions

def calculate_new_paths(path: list)-> list[list]:
    new_dirs = calculate_allowable_directions(path)
    new_paths = []
    for dir in new_dirs:
        new_pos = (path[1][0] + dir[0], path[1][1] + dir[1])
        if new_pos[0] >= WIDTH or new_pos[0] <0 or new_pos[1] >= HEIGHT or new_pos[1] <0:
            continue #we are out of range
        heat = path[0] + arr[new_pos[1]][new_pos[0]]
        new_path = [heat, new_pos, path[1], path[2], path[3]]
        new_paths.append(new_path)
    return new_paths

def check_if_at_goal(path: list)-> bool:
    pos = path[1]
    if pos[0] == WIDTH-1 and pos[1] == HEIGHT-1:
        return True
    else:
        return False

def check_saved(path: list)-> bool:
    new_dirs = calculate_allowable_directions(path)
    hashable = (path[1],*new_dirs)
    if hashable in saved_visits:
        if saved_visits[hashable] < path[0]:
            return False
        else:
            saved_visits[hashable] = path[0]
            return True
    else:
        saved_visits[hashable] = path[0]
        return True

# check the lowest heat path, and its next steps. This is easy using the heap to always look at the lowest heat scoring path
# if any are at (WIDTH, HEIGHT) we end the run - this is the shortest path

pos_heap = [[arr[1][0],(0,1),(0,0),(0,0),(0,0)],[arr[0][1],(1,0),(0,0),(0,0),(0,0)]]
heapq.heapify(pos_heap)
lowest_heat_path = None
saved_visits = {}
while True:
    if lowest_heat_path is not None:
        break
    lowest_path = heapq.heappop(pos_heap)
    new_paths = calculate_new_paths(lowest_path)
    for path in new_paths:
        #print(path)
        if not check_saved(path):
            continue
        if check_if_at_goal(path):
            lowest_heat_path = path[0]
            break
        heapq.heappush(pos_heap,path)
print(f"P1: The lowest heat path is {lowest_heat_path}")
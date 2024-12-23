from math import inf
import heapq

# a preferred q of all paths, starting with minimal heat

filename = "test_input_day_17.txt"
#filename = "test_input_day_17_2.txt"
filename = "input_day_17.txt"
arr = []
with open(filename,"r") as file:
    for line in file:
        arr.append([int(x) for x in line.replace("\n","")])

WIDTH = len(arr[0])
HEIGHT = len(arr)
print(f"The grid has shape ({WIDTH},{HEIGHT})")
# for each path, we go: [total_heat_cost, (pos), (dir)]

def return_new_dirs(path: list) -> list[list]:
    new_dirs = []
    direction = path[2]
    if direction[0] == 1 or direction[0] == -1:
        new_dirs.append((1,(0,1)))
        new_dirs.append((2,(0,1)))
        new_dirs.append((3,(0,1)))
        new_dirs.append((1,(0,-1)))
        new_dirs.append((2,(0,-1)))
        new_dirs.append((3,(0,-1)))
    else:
        new_dirs.append((1,(1,0)))
        new_dirs.append((2,(1,0)))
        new_dirs.append((3,(1,0)))
        new_dirs.append((1,(-1,0)))
        new_dirs.append((2,(-1,0)))
        new_dirs.append((3,(-1,0)))
    return new_dirs
        
def calculate_new_paths(path: list)-> list[list]:
    new_paths = []
    dir = path[2]
    new_dirs = return_new_dirs(path)    
    for dir in new_dirs:
        new_pos = (path[1][0] + dir[0]*dir[1][0], path[1][1] + dir[0]*dir[1][1])
        if new_pos[0] >= WIDTH or new_pos[0] <0 or new_pos[1] >= HEIGHT or new_pos[1] <0:
            continue #we are out of range
        heat = path[0]
        for i in range(dir[0]):
            heat += arr[path[1][1] + (i+1)*dir[1][1]][path[1][0] + (i+1)*dir[1][0]]
        #history = path[3].copy()
        #history.append(new_pos)
        new_path = [heat, new_pos, dir[1]]#, history]
        new_paths.append(new_path)

    return new_paths

def check_if_at_goal(path: list)-> bool:
    pos = path[1]
    if pos[0] == WIDTH-1 and pos[1] == HEIGHT-1:
        return True
    else:
        return False

def check_saved(path: list)-> bool:
    hashable = (path[1],path[2]) #position, direction
    if hashable in saved_visits:
        if saved_visits[hashable] <= path[0]:
            return False
        else:
            saved_visits[hashable] = path[0]
            return True
    else:
        saved_visits[hashable] = path[0]
        return True

def check_best_at_position(path: list)-> bool:
    if path[1] in best_at_pos:
        if path[0] > best_at_pos[path[1]] + 36:
            return False
        elif path[0] < best_at_pos[path[1]]:
            best_at_pos[path[1]] = path[0]
            return True
    else:
        best_at_pos[path[1]] = path[0]
        return True

# check the lowest heat path, and its next steps. This is easy using the heap to always look at the lowest heat scoring path
# if any are at (WIDTH, HEIGHT) we end the run - this is the shortest path

pos_heap = [[arr[1][0],(0,1),(0,1),[(0,0),(0,1)]],[arr[1][0]+arr[2][0],(0,2),(0,1),[(0,0),(0,2)]],[arr[1][0]+arr[2][0]+arr[3][0],(0,3),(0,1),[(0,0),(0,3)]],
            [arr[0][1],(1,0),(1,0),[(0,0),(1,0)]],[arr[0][1]+arr[0][2],(2,0),(1,0),[(0,0),(2,0)]],[arr[0][1]+arr[0][2]+arr[0][3],(3,0),(1,0),[(0,0),(3,0)]]]
#print(pos_heap)

heapq.heapify(pos_heap)
lowest_heat_path = inf
best_path = None

best_at_pos = {}
saved_visits = {}
while len(pos_heap)>0:
    lowest_path = heapq.heappop(pos_heap)
    #print(lowest_path)
    if check_if_at_goal(lowest_path):
        #print(f"Reached goal in {lowest_path[0]}")
        if lowest_heat_path > lowest_path[0]:
            lowest_heat_path = lowest_path[0]
            best_path = lowest_path
        
        continue
    new_paths = calculate_new_paths(lowest_path)
    for path in new_paths:
        if not check_saved(path):
            continue
        #if not check_best_at_position(path):
        #    continue
        heapq.heappush(pos_heap,path)

#for step in best_path[3]:
#    arr[step[1]][step[0]] = '.'

# Determine the maximum width needed for any cell
#max_width = max(len(str(item)) for row in arr for item in row)
# Format each cell with even spacing
#formatted_grid = "\n".join(" ".join(f"{str(item):<{max_width}}" for item in row) for row in arr)
#print(formatted_grid)


print(f"P1: The lowest heat path is {lowest_heat_path}")

#################### P2 ##########################

# between 4 and 10 spaces

def return_new_dirs_2(path: list) -> list[list]:
    new_dirs = []
    direction = path[2]
    if direction[0] == 1 or direction[0] == -1:
        new_dirs.extend([(i,(0,1)) for i in range(4,11)])
        new_dirs.extend([(i,(0,-1)) for i in range(4,11)])
    else:
        new_dirs.extend([(i,(1,0)) for i in range(4,11)])
        new_dirs.extend([(i,(-1,0)) for i in range(4,11)])
    return new_dirs
        
def calculate_new_paths_2(path: list)-> list[list]:
    new_paths = []
    dir = path[2]
    new_dirs = return_new_dirs_2(path)    
    for dir in new_dirs:
        new_pos = (path[1][0] + dir[0]*dir[1][0], path[1][1] + dir[0]*dir[1][1])
        if new_pos[0] >= WIDTH or new_pos[0] <0 or new_pos[1] >= HEIGHT or new_pos[1] <0:
            continue #we are out of range
        heat = path[0]
        for i in range(dir[0]):
            heat += arr[path[1][1] + (i+1)*dir[1][1]][path[1][0] + (i+1)*dir[1][0]]
        new_path = [heat, new_pos, dir[1]]#, history]
        new_paths.append(new_path)
    return new_paths


pos_heap = []
height_var = min(11,HEIGHT)
width_var = min(WIDTH,11)
#print(len(arr[0]))
for i in range(4,width_var):
    pos_heap.append([sum(arr[0][k] for k in range(1,i+1)),(i,0),(1,0)])
for i in range(4,height_var):
    pos_heap.append([sum(arr[k][0] for k in range(1,i+1)),(0,i),(0,1)])

heapq.heapify(pos_heap)
lowest_heat_path = inf
best_path = None

best_at_pos = {}
saved_visits = {}
while len(pos_heap)>0:
    lowest_path = heapq.heappop(pos_heap)
    #print(lowest_path)
    if check_if_at_goal(lowest_path):
        #print(f"Reached goal in {lowest_path[0]}")
        if lowest_heat_path > lowest_path[0]:
            lowest_heat_path = lowest_path[0]
            best_path = lowest_path
        
        continue
    new_paths = calculate_new_paths_2(lowest_path)
    for path in new_paths:
        if not check_saved(path):
            continue
        #if not check_best_at_position(path):
        #    continue
        heapq.heappush(pos_heap,path)

print(f"P2: The lowest heat path is {lowest_heat_path}")

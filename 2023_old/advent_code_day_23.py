
import re

def print_grid(arr: list[list[str]])-> None:
    max_width = max(len(str(item)) for row in arr for item in row)
    formatted_grid = "\n".join(" ".join(f"{str(item):<{max_width}}" for item in row) for row in arr)
    print(formatted_grid)

def print_path(path)-> None:
    arr2 = arr.copy()
    for node in path[2]:
        arr2[node[0]][node[1]] = "O"
    print_grid(arr2)


def find_start_and_end(arr: list[list[str]])-> ((int,int),(int,int)):
    start = (0,arr[0].index("."))
    end = (len(arr)-1,arr[-1].index("."))
    return (start, end)

def find_bordering_cells(pos: (int,int))-> list[(int,int)]:
    bordering = []
    if pos[0] != 0 and arr[pos[0]-1][pos[1]] != "#" and arr[pos[0]-1][pos[1]] != "v":
        bordering.append((pos[0]-1,pos[1]))
    if pos[0] != HEIGHT-1 and arr[pos[0]+1][pos[1]] != "#" and arr[pos[0]+1][pos[1]] != "^":
        bordering.append((pos[0]+1,pos[1]))
    if pos[0] != 0 and arr[pos[0]][pos[1]-1] != "#" and arr[pos[0]][pos[1]-1] != ">":
        bordering.append((pos[0],pos[1]-1))
    if pos[0] != WIDTH-1 and arr[pos[0]][pos[1]+1] != "#" and arr[pos[0]][pos[1]+1] != "<":
        bordering.append((pos[0],pos[1]+1))
    return bordering

def check_at_goal(path)-> bool:
    if path[1] == end:
        return True
    else:
        return False

def find_next_paths(path):
    bordering_paths = find_bordering_cells(path[1])
    new_paths = []
    for bord in bordering_paths:
        if bord in path[2]: #we have already visited
            continue
        distance = path[0]+1
        visited = path[2].copy()
        visited.add(bord)
        symbol = arr[bord[0]][bord[1]]
        if symbol in slopes:
#            print(bord)
            bord = (bord[0]+slopes[symbol][0],bord[1]+slopes[symbol][1])
#            print(bord)
            distance += 1
            visited.add(bord)

        new_paths.append((distance, bord, visited))
    return new_paths

filename = "test_input_day_23.txt"
#filename = "input_day_23.txt"
arr = []
with open(filename,"r") as file:
    for line in file:
        arr.append([c for c in line])

slopes = {"<": (0,-1),">": (0,1),"^": (-1,0), "v": (1,0)}

WIDTH = len(arr[0])
HEIGHT = len(arr)
#print_grid(arr)
(start, end) = find_start_and_end(arr)
print(f"The array has dimensions ({WIDTH},{HEIGHT})")
print(f"The goal is to go between {start}->{end}")


path_queue = [(0, start, set())] #distance, current_position, visited
longest_distance = 0
longest_path = None

while len(path_queue) > 0:
    path = path_queue.pop(0)
    #print(path)
    if check_at_goal(path):
        print(f"Reached end in {path[0]} steps")
        if path[0] > longest_distance:
            longest_distance = path[0]
            longest_path = path
        continue
    #print(find_next_paths(path))
    path_queue.extend(find_next_paths(path))


print(f"P1: The longest possible path has length {longest_distance}")
#print(longest_path)
#print_path(longest_path)

#######################################################################

def find_bordering_cells_P2(pos: (int,int))-> list[((int,int),(int,int))]:#coordinate, direction
    bordering = []
    if pos[0] != 0 and arr[pos[0]-1][pos[1]] != "#":
        bordering.append(((pos[0]-1,pos[1]),(-1,0)))
    if pos[0] != HEIGHT-1 and arr[pos[0]+1][pos[1]] != "#":
        bordering.append(((pos[0]+1,pos[1]),(1,0)))
    if pos[0] != 0 and arr[pos[0]][pos[1]-1] != "#":
        bordering.append(((pos[0],pos[1]-1),(0,-1)))
    if pos[0] != WIDTH-1 and arr[pos[0]][pos[1]+1] != "#":
        bordering.append(((pos[0],pos[1]+1),(0,1)))
    return bordering

def find_next_paths_P2(path):
    bordering_paths = find_bordering_cells_P2(path[1])
    new_paths = []
    for bord in bordering_paths:
        if bord[0] in path[2]: #we have already visited
            continue
        distance = path[0]+1
        visited = path[2].copy()
        visited.add(bord[0])

        
        new_paths.append((distance, bord, visited))
    if len(new_paths) == 0:#dead end
        junction_set[path[3]] = 0
    elif len(new_paths) == 1: #normal path
        pass
    elif len(new_paths) == 2 or len(new_paths) == 3: # junction
        junction_set[path[3]] = path[0] 
    else:
        raise ValueError
    return new_paths

path_queue = [(0, start, set()),()] #distance, current_position, visited, (last_junction, direction)
junction_set = {}
# a zero means a deadend
longest_distance = 0
longest_path = None

while len(path_queue) > 0:
    path = path_queue.pop(0)
    #if only one path do something?
    #print(path)
    if check_at_goal(path):
        print(f"Reached end in {path[0]} steps")
        if path[0] > longest_distance:
            longest_distance = path[0]
            longest_path = path
        continue
    #print(find_next_paths(path))
    #print(path_queue)
    path_queue.extend(find_next_paths_P2(path))

print(f"P2: The longest possible path has length {longest_distance}")
#print(longest_path)
#print_path(longest_path)

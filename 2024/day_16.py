from typing import List

class Coordinate():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        
    def __add__(self, other):
        return Coordinate(self.x+other.x, self.y+other.y)
    
    def __repr__(self):
        return f"({self.x},{self.y})"
    
    def __hash__(self):
        return hash((self.x,self.y))
    
    def __eq__(self, other):
        if self.x==other.x and self.y == other.y:
            return True
        return False


class Grid():
    def __init__(self, data):
        self.data = data
        for y, line in enumerate(data):
            for x, char in enumerate(line):
                if char == "E":
                    self.exit = Coordinate(x, y)
                elif char == "S":
                    self.entry = Coordinate(x, y)
    def __repr__(self):
        string = ""
        for line in data:
            string += line+"\n"
        return string
    
    def get_coordinate(self, coord: Coordinate):
        return self.data[coord.y][coord.x]

    def set_coordinate(self, coord: Coordinate, icon: str):
        new_line = ""
        for x, c in enumerate(self.data[coord.y]):
            if x==coord.x:
                new_line+=icon
            else:
                new_line+=c
        self.data[coord.y] = new_line

def bfs_path_to_start(pos: Coordinate, dir: Coordinate, cache, cost_to_here: int, seen_on_route: List[Coordinate]):
    seen_on_route.append(pos)
    hashed = hash((pos, dir))
    if pos == grid.entry:
        print(cost_to_here)
    if hashed in cache:
        if cost_to_here <= cache[hashed]: # less than or equal makes this much less efficient but is needed for part 2
            cache[hashed] = cost_to_here
        else:
            return []
    else:
        cache[hashed] = cost_to_here
        # print(pos, cost_to_here)

    paths = []
    if grid.get_coordinate(pos+dir) == 'E':
        cache[hash((pos+dir,dir))] = cost_to_here+1
        seen_on_route.append(pos+dir)
        return (seen_on_route, cost_to_here+1)
    elif grid.get_coordinate(pos+dir) == '.':
        paths.append((pos+dir, dir, cost_to_here+1, seen_on_route.copy()))
    for d in turn_dir_map[dir]:
        pt = grid.get_coordinate(pos+d)
        if pt == 'E':
            cache[hash((pos+d,d))] = cost_to_here+1001
            seen_on_route.append(pos+d)
            return (seen_on_route, cost_to_here+1001)
        elif pt == '.':
            paths.append((pos+d, d, cost_to_here+1001, seen_on_route.copy()))

    return paths

input_file = "2024/inputs/day_16_input.txt"
# input_file = "2024/inputs/day_16_example.txt"
# input_file = "2024/inputs/day_16_example_2.txt"

data = []
with open(input_file,'r') as file_in:
    for line in file_in:
        data.append(line.rstrip())

turn_dir_map = {
    Coordinate(0,1): [Coordinate(-1,0), Coordinate(1,0)],
    Coordinate(0,-1): [Coordinate(1,0), Coordinate(-1,0)],
    Coordinate(1,0): [Coordinate(0,-1), Coordinate(0,1)],
    Coordinate(-1,0): [Coordinate(0,1), Coordinate(0,-1)]
}
icons = {
    Coordinate(0,1): "v",
    Coordinate(0,-1): "^",
    Coordinate(1,0): ">",
    Coordinate(-1,0): "<"
}

grid = Grid(data)

start_pos = grid.entry
end_pos = grid.exit
start_orientation = Coordinate(1,0)

cache = {} # pos, orientation

# print(get_cost_to_end(start_pos, start_orientation, cache, cost_in, 0, turn_dir_map))
paths = [(start_pos, Coordinate(1,0),0, [start_pos])]

best_cost = 1e10
paths_to_end = []
while len(paths)>0:
    new_paths = []
    for pos, dir, cost, seen in paths:
        if cost>best_cost:
            continue
        np = bfs_path_to_start(pos, dir, cache, cost, seen)
        if len(np)!=0:
            if len(np[0]) == 4:
                new_paths.extend(np)
            else:
                paths_to_end.append((np[1],np[0]))
                best_cost = min(best_cost, np[1])
    paths = new_paths

route_scores = []
for key in icons:
    hash_end = hash((grid.exit, key))
    if hash_end in cache:
        route_scores.append(cache[hash_end])

print(f"The answer to part 1 is {min(route_scores)}")

seen_on_best = set()
for p in paths_to_end:
    if p[0] == best_cost:
        seen_on_best.update(set(p[1]))

print(f"The answer to part 2 is {len(seen_on_best)}")


# 129536 too low
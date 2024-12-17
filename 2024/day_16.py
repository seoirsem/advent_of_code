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


def dfs_path_to_end(pos: Coordinate, dir: Coordinate, cache, this_route):
    hashed = hash((pos, dir))
    if hashed in cache:
        return cache[hashed]
    
    if pos in this_route: #already visited
        return 1e10, this_route
    else:
        this_route.add(pos)
    
    # recursively try all paths from here
    paths = []
    if grid.get_coordinate(pos+dir) == 'E':
        return 1, this_route
    elif grid.get_coordinate(pos+dir) == '.':
        paths.append((pos+dir, dir, 1))

    for d in turn_dir_map[dir]:
        pt = grid.get_coordinate(pos+d)
        if pt == 'E':
            return 1001, this_route
        elif pt == '.':
            paths.append((pos+d, d, 1001))

    if len(paths) == 0:
        return 1e10, this_route
    costs = []
    routes = []
    for p, d, c in paths:
        cost, route = dfs_path_to_end(p, d, cache, this_route.copy())
        costs.append(cost+c)
        routes.append(route)

    this_route = routes[costs.index(min(costs))]
    cache[hashed] = (min(costs), this_route)
    return min(costs), this_route

def bfs_path_to_start(pos: Coordinate, dir: Coordinate, cache, cost_to_here: int):
    hashed = hash((pos, dir))
    if pos == grid.entry:
        print(cost_to_here)
    if hashed in cache:
        if cost_to_here < cache[hashed]:
            cache[hashed] = cost_to_here
        else:
            return []
    else:
        cache[hashed] = cost_to_here

    paths = []
    if grid.get_coordinate(pos+dir) == 'S':
        return []
    elif grid.get_coordinate(pos+dir) == '.':
        paths.append((pos+dir, dir, cost_to_here+1))
    for d in turn_dir_map[dir]:
        pt = grid.get_coordinate(pos+d)
        if pt == 'S':
            return []
        elif pt == '.':
            paths.append((pos+d, d, cost_to_here+1001))

    return paths

input_file = "2024/inputs/day_16_input.txt"
input_file = "2024/inputs/day_16_example.txt"
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
paths = [(end_pos, Coordinate(-1,0),0), (end_pos, Coordinate(0,-1), 0)]
while len(paths)>0:
    new_paths = []
    for pos, dir, cost in paths:
        new_paths.extend(bfs_path_to_start(pos, dir, cache, cost))
    paths = new_paths


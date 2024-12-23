from collections import Counter

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
        self.xlim=len(data[0])
        self.ylim=len(data)
        self.dirs = [Coordinate(0,1), Coordinate(0,-1), Coordinate(1,0), Coordinate(-1,0)]

    def __repr__(self):
        string = ""
        for line in data:
            string += line+"\n"
        return string
    
    def get_coordinate(self, coord: Coordinate):
        if coord.x<0 or coord.x>=self.xlim or coord.y<0 or coord.y>=self.ylim:
            return
        return self.data[coord.y][coord.x]

    def set_coordinate(self, coord: Coordinate, icon: str):
        new_line = ""
        for x, c in enumerate(self.data[coord.y]):
            if x==coord.x:
                new_line+=icon
            else:
                new_line+=c
        self.data[coord.y] = new_line

    def get_all_available(self, coord: Coordinate):
        available = []
        for direction in self.dirs:
            if self.get_coordinate(coord+direction) in ['.','S','E']:
                available.append(coord+direction)
        return available

    def get_in_range_20(self, coord: Coordinate):
        available = set()
        for dx in range(-20,21):
            for dy in range(-20+abs(dx),21-abs(dx)):
                new_c=coord+Coordinate(dx,dy)
                if self.get_coordinate(new_c) in ['.','S','E']:
                    available.add((new_c,abs(dx)+abs(dy)))
        return list(available)

def search_routes(position, grid, cost_to_here, cache):
    new_ps = grid.get_all_available(position)
    next_layer = []
    for new_p in new_ps:
        if new_p in cache:
            if cost_to_here+1 < cache[new_p]:
                cache[new_p] = cost_to_here+1
                next_layer.append((new_p,cost_to_here+1))
        else:
            cache[new_p] = cost_to_here+1
            next_layer.append((new_p,cost_to_here+1))
    return next_layer


input_file = "2024/inputs/day_20_input.txt"
# input_file = "2024/inputs/day_20_example.txt"

data = []
with open(input_file,'r') as file_in:
    for line in file_in:
        data.append(line.rstrip())


grid = Grid(data)

start_pos = grid.entry
end_pos = grid.exit
start_orientation = Coordinate(1,0)

cache_s = {grid.entry: 0} # pos: dist to start
cache_e = {grid.exit: 0} # pos: dist to end


paths = [(start_pos,0)]
while len(paths)>0:
    new_paths = []
    for p, cost in paths:
        new_paths.extend(search_routes(p,grid,cost, cache_s))
    paths = new_paths
paths = [(end_pos,0)]
while len(paths)>0:
    new_paths = []
    for p, cost in paths:
        new_paths.extend(search_routes(p,grid,cost, cache_e))
    paths = new_paths

best_path = cache_s[grid.exit]
cost_savings = Counter()
big_cost_savings = Counter()
for x in range(1,grid.xlim-1):
    for y in range(1,grid.ylim-1):
        c = Coordinate(x,y)
        if grid.get_coordinate(c) in ['.','E','S']:
            for d in grid.dirs:
                skip_p = c+d+d
                if grid.get_coordinate(skip_p) in ['.','E','S']:
                    cost = cache_s[c]+cache_e[skip_p]+2
                    if cost<best_path:
                        cost_savings[best_path-cost]+=1
            #big cheat here
            for d_skip, dcost in grid.get_in_range_20(c):
                cost = cache_s[c]+cache_e[d_skip]+dcost
                if cost<best_path:
                        big_cost_savings[best_path-cost]+=1

more_than_100=0
for c in cost_savings:
    if c>=100:
        more_than_100+=cost_savings[c]
print(f"The answer to part 1 is {more_than_100}")

more_than_100=0
for c in big_cost_savings:
    if c>=100:
        more_than_100+=big_cost_savings[c]
print(f"The answer to part 2 is {more_than_100}")


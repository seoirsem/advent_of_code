from collections import defaultdict

class Coordinate():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
    
    def __sub__(self, other):
        return Coordinate(self.x-other.x, self.y-other.y)
    
    def __add__(self, other):
        return Coordinate(self.x+other.x, self.y+other.y)
    
    def __str__(self):
        return f"Coordinate({self.x},{self.y})"
    
    def __repr__(self):
        return f"Coordinate({self.x},{self.y})"
    
    def __hash__(self):
        return hash((self.x,self.y))
    
    def __eq__(self, other):
        if self.x==other.x and self.y == other.y:
            return True
        return False


class Topo():
    def __init__(self, data) -> None:
        self.data = data
        self.xlim = len(data[0])
        self.ylim = len(data)
        self.main_dirs = [Coordinate(0,1), Coordinate(0,-1), Coordinate(1,0), Coordinate(-1,0)]

    def get_val(self, coord: Coordinate):
        if coord.x >= self.xlim or coord.y >= self.ylim or coord.x < 0 or coord.y <0:
            return None
        return self.data[coord.y][coord.x]
    
    def find_in_surround(self, coord, value):
        points = []
        for dir in self.main_dirs:
            new_c = coord+dir
            if self.get_val(new_c) == value:
                points.append(new_c)
        return points

    def iter(self):
        for y in range(self.ylim):
            for x in range(self.xlim):
                yield Coordinate(x, y)

input_file="day_10_input.txt"
# input_file="day_10_example.txt"

data = []
with open(input_file,'r') as input:
    for line in input:
        data.append([int(x) for x in line.rstrip()])

top = Topo(data)

iter = top.iter()
accessable = defaultdict(set)
path_counts_start = defaultdict(int)
for coord in iter:
    if top.get_val(coord) == 9:
        eights = top.find_in_surround(coord,8)
        if len(eights)>0:
            for eight in eights:
                accessable[eight].add(coord)
                path_counts_start[eight] += 1

for i in range(7,-1,-1):
    new_acc = defaultdict(set)
    path_counts = defaultdict(int)
    for coordinate, nine_list in accessable.items():
        next_vals = top.find_in_surround(coordinate, i)
        if len(next_vals)>0:
            for val in next_vals:
                path_counts[val] += path_counts_start[coordinate]
                for x in nine_list:
                    new_acc[val].add(x)
    accessable = new_acc
    path_counts_start = path_counts

trailhead_sum = 0
for _, nine_accesses in accessable.items():
    trailhead_sum += len(set(nine_accesses))

print(f"The answer to part 1 is {trailhead_sum}")

trailhead_sum = 0
for _, nine_path_count in path_counts_start.items():
    trailhead_sum += nine_path_count

print(f"The answer to part 2 is {trailhead_sum}")


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
    def __init__(self, data, xlim, ylim):
        self.xlim = xlim
        self.ylim = ylim
        self.grid = [['.' for _ in range(xlim)] for _ in range(ylim)]
        for c in data:
            self.set_coordinate(c, '#')

    def __repr__(self):
        string = ""
        for line in self.grid:
            string += "".join(line)+"\n"
        return string
    
    def get_coordinate(self, coord: Coordinate):
        if coord.x < 0 or coord.x >= self.xlim or coord.y < 0 or coord.y >= self.ylim:
            return
        return self.grid[coord.y][coord.x]

    def set_coordinate(self, coord: Coordinate, icon: str):
        self.grid[coord.y][coord.x] = icon
    
    def get_available(self, coord: Coordinate):
        
        directions = [Coordinate(0,1),
              Coordinate(0,-1),
              Coordinate(1,0),
              Coordinate(-1,0)
              ]
        dir_out = []
        for dir in directions:
            if self.get_coordinate(coord+dir) == '.':
                dir_out.append(coord+dir)
        return dir_out

def search_for_path(grid: Grid):
    start=Coordinate(0,0)
    visited = set()
    visited.add(start)
    target=Coordinate(xlim-1,ylim-1)
    to_try=grid.get_available(start)

    steps=1
    while len(to_try)>0:
        new_nodes = []
        for c in to_try:
            if c==target:
                return steps
            if c in visited:
                continue
            new_nodes.extend(grid.get_available(c))
            visited.add(c)
        steps+=1
        to_try = new_nodes
    return None


example = False
if example:
    input_file = "2024/inputs/day_18_example.txt"
    xlim = 7
    ylim = 7
    n_in = 12
else:
    input_file = "2024/inputs/day_18_input.txt"
    xlim = 71
    ylim = 71
    n_in = 1024

coords = []
with open(input_file, 'r') as f_in:
    for i,line in enumerate(f_in):
        coords.append(Coordinate(*[int(x) for x in line.rstrip().split(',')]))
grid_pt1 = Grid(coords[0:n_in], xlim, ylim)


print(f"The answer to part 1 is {search_for_path(grid_pt1)}")

# small enough for brute force
grid = Grid(coords[0:n_in], xlim, ylim)
for byte in coords[n_in:]:
    grid.set_coordinate(byte,'#')
    if search_for_path(grid) is None:
        break
print(f"The answer to part 2 is {byte}")

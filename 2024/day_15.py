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

class Warehouse():
    def __init__(self, warehouse):
        self.data = warehouse
        self.xlim = len(warehouse[0])
        self.ylim = len(warehouse)
        for y, line in enumerate(self.data):
            for x, pt in enumerate(line):
                if pt == "@":
                    self.robot = Coordinate(x, y)
    
    def get_position(self, position: Coordinate):
        if position.x >= self.xlim or position.y >= self.ylim or position.x < 0 or position.y <0:
            return None
        return self.data[position.y][position.x]

    def get_gps_score(self):
        score = 0
        for y, line in enumerate(self.data):
            for x, c in enumerate(line):
                if c == "O":
                    score += (100*y) + x
        return score

    def set_position(self, position: Coordinate, value: str):
        self.data[position.y][position.x] = value

    def __repr__(self):
        return "".join(["".join([x for x in line]) + "\n" for line in self.data])
    
    def find_next_open(self, position: Coordinate, direction: Coordinate):
        pt = position
        pt_type = self.get_position(pt)
        while pt_type != ".":
            pt = pt + direction
            pt_type = self.get_position(pt)
            if pt_type in [None, '#']:
                return None
        return pt
    
    def step_robot(self, direction: Coordinate):
        next_open = self.find_next_open(self.robot, direction)
        if next_open is None:
            return
        elif next_open == self.robot+direction: # open space
            self.set_position(self.robot, '.')
            self.set_position(self.robot+direction, '@')
            self.robot += direction
        else: # shift boxes
            self.set_position(next_open,'O')
            self.set_position(self.robot, '.')
            self.set_position(self.robot+direction, '@')
            self.robot += direction


def load_data(input_file):
    data = []
    movements = ""
    with open(input_file,'r') as file_in:
        for line in file_in:
            if "<" in line or ">" in line:
                movements+=line.rstrip()
            elif line != "\n":
                data.append([x for x in line.rstrip()])
    return data, movements

class Warehouse2():
    def __init__(self, warehouse):
        self.xlim = len(warehouse[0]*2)
        self.ylim = len(warehouse)
        self.data = []
        for y, line in enumerate(warehouse):
            line_data = []
            for x, pt in enumerate(line):
                if pt == "#":
                    line_data.extend(['#','#'])
                elif pt == "O":
                    line_data.extend(['[',']'])
                elif pt == ".":
                    line_data.extend(['.','.'])
                elif pt == "@":
                    self.robot = Coordinate(x*2, y)
                    line_data.extend(['@','.'])
            self.data.append(line_data)

    def get_position(self, position: Coordinate):
        if position.x >= self.xlim or position.y >= self.ylim or position.x < 0 or position.y <0:
            return None
        return self.data[position.y][position.x]

    def get_gps_score(self):
        score = 0
        for y, line in enumerate(self.data):
            for x, c in enumerate(line):
                if c == "[":
                    score += (100*y) + x
        return score

    def set_position(self, position: Coordinate, value: str):
        self.data[position.y][position.x] = value

    def __repr__(self):
        return "".join(["".join([x for x in line]) + "\n" for line in self.data])
    
    def step_x(self, position: Coordinate, direction: Coordinate):
        pt = Coordinate(position.x, position.y)
        pt_type = self.get_position(pt)
        while pt_type != ".":
            pt = pt + direction
            pt_type = self.get_position(pt)
            if pt_type in [None, '#']:
                return
        neg_dir = Coordinate(-direction.x, 0)
        while pt != position:
            self.set_position(pt, self.get_position(pt+neg_dir))
            pt += neg_dir
        self.set_position(position,'.') 
        self.robot += direction
        return pt

    def check_next(self, position, direction):
        pt = self.get_position(position+direction)        
        if pt == '#':
            return None
        elif pt == '.':
            return []
        elif pt == '[':
            return set([position+direction, position+direction+Coordinate(1,0)])
        else: #']'
            return set([position+direction, position+direction+Coordinate(-1,0)])
        

    def step_y(self, position: Coordinate, direction: Coordinate):
        next_row = self.check_next(position, direction)
        if next_row is None:
            return

        all_moves = [set([position])] # start row
        while len(next_row) > 0:
            next_row_new = set()
            for p in next_row:
                additional = self.check_next(p, direction)
                if additional is None:
                    return # hit a wall
                next_row_new.update(additional)
            all_moves.append(next_row)
            next_row = next_row_new
        
        for moves in range(len(all_moves)-1, -1, -1):
            for move in all_moves[moves]:
                self.set_position(move+direction,self.get_position(move))
                self.set_position(move,'.')
        
        self.robot = self.robot + direction
        pass



    def step_robot(self, direction: Coordinate):
        if direction.x != 0:
            self.step_x(self.robot, direction)
        else:
            self.step_y(self.robot, direction)
        
input_file = "2024/inputs/day_15_example.txt"
input_file = "2024/inputs/day_15_example_2.txt"
input_file = "2024/inputs/day_15_input.txt"


dir_map = { 
    "^": Coordinate(0,-1),
    "<": Coordinate(-1,0),
    ">": Coordinate(1,0),
    "v": Coordinate(0,1),
}

data, movements = load_data(input_file)
warehouse = Warehouse(data)
for d in movements:
    warehouse.step_robot(dir_map[d])
print(f"The answer to part 1 is {warehouse.get_gps_score()}")

data, movements = load_data(input_file)
warehouse = Warehouse2(data)
for d in movements:
    warehouse.step_robot(dir_map[d])
print(f"The answer to part 2 is {warehouse.get_gps_score()}")
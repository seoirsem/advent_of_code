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
    
class PerimeterEdge():
    def __init__(self, start: Coordinate, end: Coordinate, dir: Coordinate):
        self.start = start # average of points either side
        self.end = end
        self.dir = dir
    def __hash__(self):
        return hash((self.start.x, self.start.y, self.end.x, self.end.y, self.dir.y, self.dir.x))
    
    def __eq__(self, other):
        return self.start == other.start and self.end == other.end and self.dir == other.dir

    def __repr__(self):
        return f"Perimeter: {self.start}, {self.end}, {self.dir}"

class Farm():
    def __init__(self, data) -> None:
        self.data = data
        self.xlim = len(data[0])
        self.ylim = len(data)
        self.main_dirs = [Coordinate(0,1), Coordinate(0,-1), Coordinate(1,0), Coordinate(-1,0)]

        self.in_field = set()
        self.area_perimeter = {} # id: (area*perimeter)

    def get_val(self, coord: Coordinate):
        if coord.x >= self.xlim or coord.y >= self.ylim or coord.x < 0 or coord.y <0:
            return None
        return self.data[coord.y][coord.x]
        
    def get_neighbours_eq(self, coord: Coordinate, value: str):
        neighbours = []
        perimiters = []
        for dir in self.main_dirs:
            new_coord = coord+dir
            if self.get_val(new_coord) == value:
                neighbours.append(new_coord)
            else:
                perimiters.append(PerimeterEdge(
                    Coordinate(coord.x + dir.x/2 + dir.y/2,coord.y+dir.y/2+dir.x/2),
                    Coordinate(coord.x + dir.x/2 - dir.y/2,coord.y+dir.y/2-dir.x/2),
                    dir
                    ))
        return neighbours, perimiters
    
    def find_field_extents(self, start: Coordinate):
        search_stack = [start]
        perimeters = []
        self.in_field.add(start)
        value = self.get_val(start)
        area = 0
        perimeter = 0
        while len(search_stack) > 0:
            new_segments, pers = self.get_neighbours_eq(search_stack.pop(-1), value)
            perimeters.extend(pers)
            area += 1
            perimeter += 4-len(new_segments)
            for seg in new_segments:
                if seg not in self.in_field:
                    self.in_field.add(seg)
                    search_stack.append(seg)
        return area, perimeter, self.get_new_perimeter(perimeters)

    def get_new_perimeter(self, perimeters: List[PerimeterEdge]):
        no_change = False
        while no_change == False:
            no_change = True
            for idx, p in enumerate(perimeters):
                for jdx, q in enumerate(perimeters[idx+1:]):
                    if p.dir == q.dir:
                        if p.start == q.start:
                            p.start = q.end
                            no_change = False
                            perimeters.pop(jdx+idx+1)
                        elif p.start == q.end:
                            p.start = q.start
                            no_change = False
                            perimeters.pop(jdx+idx+1)
                        elif p.end == q.start:
                            p.end = q.end
                            no_change = False
                            perimeters.pop(jdx+idx+1)
                        elif p.end == q.end:
                            p.end = q.start
                            no_change = False
                            perimeters.pop(jdx+idx+1)
                    if not no_change:
                        break
                if not no_change:
                    break
        return len(perimeters)
            
    def get_all_fields(self):
        sum_extents = 0
        sum_new_extents = 0
        for x in range(self.xlim):
            for y in range(self.ylim):
                coord = Coordinate(x, y)
                if coord not in self.in_field:
                    area, perimeter, new_perimeters = self.find_field_extents(coord)
                    sum_new_extents += area*new_perimeters
                    sum_extents += area*perimeter

        return sum_extents, sum_new_extents
    
input_file = "day_12_example.txt"
input_file = "day_12_input.txt"

with open(input_file,'r') as input:
    field_data = []
    for line in input:
        field_data.append(line.rstrip())

farm = Farm(field_data)
extents_1, extents_2 = farm.get_all_fields()
print(f"The answer to part 1 is {extents_1}")
print(f"The answer to part 2 is {extents_2}")
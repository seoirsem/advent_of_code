from collections import defaultdict
from math import gcd

class Coordinate():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
    
    def __sub__(self, other):
        return Coordinate(self.x-other.x, self.y-other.y)
    
    def __add__(self, other):
        return Coordinate(self.x+other.x, self.y+other.y)
    
    def antinodes(self, other, xlim: int, ylim: int):
        antinodes = []
        x1 = 2*self.x-other.x
        y1 = 2*self.y-other.y
        if x1 >= 0 and x1 < xlim and y1 >=0 and y1 < ylim:
            antinodes.append(Coordinate(x1, y1))
        x2 = 2*other.x-self.x
        y2 = 2*other.y-self.y
        if x2 >= 0 and x2 < xlim and y2 >=0 and y2 < ylim:
            antinodes.append(Coordinate(x2, y2))
        return antinodes
    
    def in_bounds(self, xlim, ylim):
        if self.x >=0 and self.x < xlim and self.y>=0 and self.y<ylim:
            return True
        return False

    def harmonic_antinodes(self, other: "Coordinate", xlim: int, ylim: int):
        dx = self.x - other.x
        dy = self.y - other.y
        gcom = gcd(dx, dy)
        dx = dx//gcom
        dy = dy//gcom
        antinodes = set([self, other])
        i = 0
        while True:
            pt = self + Coordinate(i*dx, i*dy)
            if pt.in_bounds(xlim, ylim):
                antinodes.add(pt)
                i+=1
            else:
                break
        i=0
        while True:
            pt = self - Coordinate(i*dx, i*dy)
            if pt.in_bounds(xlim, ylim):
                antinodes.add(pt)
                i+=1
            else:
                break
        return antinodes
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

class ArrayData():
    def __init__(self, data):
        self.data = data
        self.ylim = len(self.data)
        self.xlim = len(self.data[0])

        self.unique_symbols = set()
        for line in data:
            for sym in line:
                if sym != '.':
                    self.unique_symbols.add(sym)

        self.symbol_locations = defaultdict(list)
        for symbol in self.unique_symbols:
            for y in range(len(self.data)):
                for x in range(len(self.data[y])):
                    if self.data[y][x] == symbol:
                        self.symbol_locations[symbol].append(Coordinate(x,y))

    def set_coord(self,coord, string):
        self.data[coord.y] = self.data[coord.y][0:coord.x] + string + self.data[coord.y][coord.x+1:]

    def __str__(self):
        return "\n".join(self.data)
    
    def get_coord(self,x,y):
        return self.data[y][x]

    def get_symbols(self):
        return list(self.unique_symbols)
    
    def get_all(self, symbol: str):
        if symbol not in self.unique_symbols:
            return None
        return self.symbol_locations[symbol]
    
    def get_antinodes(self):
        antinodes = set()
        for symbol in self.get_symbols():
            points = self.get_all(symbol)
            for i in range(len(points)-1):
                for j in range(i+1,len(points)):
                    for x in points[i].antinodes(points[j], self.xlim, self.ylim):
                        antinodes.add(x)
        return antinodes
    
    def get_harmonic_antinodes(self):
        antinodes = set()
        for symbol in self.get_symbols():
            points = self.get_all(symbol)
            for i in range(len(points)-1):
                for j in range(i+1,len(points)):
                    for x in points[i].harmonic_antinodes(points[j], self.xlim, self.ylim):
                        antinodes.add(x)
        return antinodes
input_file = "day_8_input.txt"
# input_file = "day_8_example.txt"

data = []
with open(input_file,'r') as input:
    for line in input:
        data.append(line.rstrip())

array = ArrayData(data)
antinodes = array.get_antinodes()

print(f"The answer to part 1 is {len(antinodes)}")

harmonic_antindoes = array.get_harmonic_antinodes()

print(f"The answer to part 2 is {len(harmonic_antindoes)}")

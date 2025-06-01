from typing import Tuple, List
from dataclasses import dataclass


@dataclass
class Coordinate():
    x: int
    y: int

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Coordinate(x,y)

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            return NotImplemented

        return Coordinate(self.x*other, self.y*other)

class XmasArray():
    def __init__(self, data: List[str]):
        self.data = data
        self.xlim = len(data[0])
        self.ylim = len(data)
    
    def get_coord(self, pt: Coordinate):
        x = pt.x
        y = pt.y
        if x < 0 or x >= self.xlim or y < 0 or y >= self.ylim:
            return None
        return self.data[y][x]
    
    def check_xmas(self, start_idx: Coordinate, vector: Coordinate):
        string = ""
        for i in range(4):
            v = self.get_coord(start_idx + vector*i)
            if v is None:
                return False
            string+=v
        if string == "XMAS":
            return True
        else:
            return False
    
    def check_point(self, start_idx: Coordinate):
        xmas_count = 0
        if self.get_coord(start_idx)!= "X":
            return 0
        for x in [-1,0,1]:
            for y in [-1,0,1]:
                if x==y and x==0:
                    continue
                xmas_count+=self.check_xmas(start_idx, Coordinate(x,y))
        return xmas_count

    def check_array(self):
        total_xmas = 0
        for x in range(self.xlim):
            for y in range(self.ylim):
                total_xmas+=self.check_point(Coordinate(x,y))
        return total_xmas

class X_MasArray():

    def __init__(self, data: List[str]):
        self.data = data
        self.xlim = len(data[0])
        self.ylim = len(data)
    
    def get_coord(self, pt: Coordinate):
        x = pt.x
        y = pt.y
        if x < 0 or x >= self.xlim or y < 0 or y >= self.ylim:
            return None
        return self.data[y][x]
    
    def check_x_mas(self, start_idx: Coordinate):
        if self.get_coord(start_idx) != "A":
            return False
        left = set([self.get_coord(start_idx+Coordinate(-1,-1)),self.get_coord(start_idx+Coordinate(1,1))])
        right = set([self.get_coord(start_idx+Coordinate(1,-1)),self.get_coord(start_idx+Coordinate(-1,1))])
        target = set("MS")
        if left == target and right == target:
            return True
        return False
    
    def check_array(self):
        total_xmas = 0
        for x in range(self.xlim):
            for y in range(self.ylim):
                total_xmas+=self.check_x_mas(Coordinate(x,y))
        return total_xmas


file_in = "day_4_input.txt"
data = []
with open(file_in, 'r') as input:
    for line in input:
        data.append(line.rstrip())

test_data = [
    "MMMSXXMASM",
    "MSAMXMSMSA",
    "AMXSXMAAMM",
    "MSAMASMSMX",
    "XMASAMXAMM",
    "XXAMMXXAMA",
    "SMSMSASXSS",
    "SAXAMASAAA",
    "MAMMMXMMMM",
    "MXMXAXMASX"
    ]


x_arr = XmasArray(data)
print(f"The answer to part 1 is {x_arr.check_array()}")

x_arr = X_MasArray(data)

print(f"The answer to part 2 is {x_arr.check_array()}")

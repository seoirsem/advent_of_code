import argparse

class Grid:
    def __init__(self, input: list[str]):
        self.inputs = input
        self.lenx = len(input[0])
        self.leny = len(input)
    
    def get_xrange(self, y, x1, x2):
        if y < 0 or y>=self.leny:
            return None
        if x1>self.leny or x2 < 0:
            return None
        if x1>x2:
            return None
        return self.inputs[y][max(x1,0):min(x2,self.lenx)+1]

    def is_free(self, x: int, y: int):
        if self.inputs[y][x] != "@":
            return False
        count = 0
        for ys in [y-1, y, y+1]:
            strip = self.get_xrange(ys,x-1,x+1)
            if not strip:
                continue
            count+= strip.count("@")
        if count > 4:
            return False
        return True

    def grid_free(self):
        count = 0
        for x in range(self.lenx):
            for y in range(self.leny):
                count += self.is_free(x,y)
        return count

class Grid2:
    def __init__(self, input: list[str]):
        self.inputs = input
        self.inputs = [[char for char in line] for line in input]
        self.lenx = len(input[0])
        self.leny = len(input)
        self.freed_list = set()
    
    def get_xrange(self, y, x1, x2):
        if y < 0 or y>=self.leny:
            return None
        if x1>self.leny or x2 < 0:
            return None
        if x1>x2:
            return None
        return self.inputs[y][max(x1,0):min(x2,self.lenx)+1]

    def get_tile(self, x, y):
        if x < 0 or x >= self.lenx:
            return None
        if y < 0 or y >= self.leny:
            return None
        return self.inputs[y][x]

    def get_roll_neighbours(self, x, y):
        list_out = []
        for x1 in [x-1,x,x+1]:
            for y1 in [y-1,y,y+1]:
                if self.get_tile(x1,y1) == "@":
                    list_out.append((x1,y1))
        return list_out

    def is_free(self, x: int, y: int):
        if self.inputs[y][x] != "@":
            return False
        count = 0
        for ys in [y-1, y, y+1]:
            strip = self.get_xrange(ys,x-1,x+1)
            if not strip:
                continue
            count+= strip.count("@")
        if count > 4:
            return False
        self.inputs[y][x] = "x"
        self.freed_list.update(self.get_roll_neighbours(x,y))
        return True

    def grid_free_rec(self):
        count = 0
        for x in range(self.lenx):
            for y in range(self.leny):
                count += self.is_free(x,y)
        while len(self.freed_list) > 0:
            element = self.freed_list.pop()
            
            count+= self.is_free(*element)
        return count

           
test_input = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

def main(test: bool=True):
    if test:
        input = test_input.split("\n")
    else:
        input = [x.strip() for x in open("2025/data_4.txt")]
    inp_cls = Grid(input)
    print(f"The answer to part 1 is {inp_cls.grid_free()}")
    inp_cls2 = Grid2(input)
    print(f"The answer to part 2 is {inp_cls2.grid_free_rec()}")
    
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(test=args.test)

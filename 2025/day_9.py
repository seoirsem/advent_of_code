import argparse
from time import time
start = time()

test_input = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

def get_area(coorda, coordb):
    return abs((coorda[0]-coordb[0]+1)*(coorda[1]-coordb[1]+1))


class Boundary:
    # Left, Up, Right, Down
    def __init__(self, start, end, direction: int = -1):
        self.start = start
        self.end = end
        self.diffx = start[0] - end[0]
        self.diffy = start[1] - end[1]
        self.vertical = self.diffy != 0

        self.direction = direction
            
    def get_sorted_x(self):
        if self.start[0] >= self.end[0]:
            return [self.end[0], self.start[0]]
        return [self.start[0], self.end[0]]
    
    def __eq__(self, value: object, /) -> bool:
        if self.start == value.start and self.end == value.end:
            return True
        return False

    def get_sorted_y(self):
        if self.start[1] >= self.end[1]:
            return [self.end[1], self.start[1]]
        return [self.start[1], self.end[1]]
    
    def test_internal(self, point):
        # project a line count intersections
        pass

    def intersect(self, other_line):
        if self.start in [other_line.start, other_line.end]:
            return None
        if self.end in [other_line.start, other_line.end]:
            return None
        # is parallel
        if self.vertical == other_line.vertical:
            return None

        # other line crosses in x (9, 5) (2, 5) | (9, 7) (9, 3)   
        if self.vertical:
            sorted_y = self.get_sorted_y()
            other_y = other_line.start[1]
            if other_line.end[0] > other_line.start[0]:
                if other_y > sorted_y[1] or other_y <= sorted_y[0]:
                    return None
            else:
                if other_y >= sorted_y[1] or other_y < sorted_y[0]:
                    return None
            other_sort = other_line.get_sorted_x()
            if self.start[0] < other_sort[0] or self.start[0] > other_sort[1]:
                return None
            return (self.start[0], other_y)
        sorted_x = self.get_sorted_x()
        other_x = other_line.start[0]
        if other_line.end[1] > other_line.start[1]:
            if other_x >= sorted_x[1] or other_x < sorted_x[0]:
                return None
        else:
            if other_x > sorted_x[1] or other_x <= sorted_x[0]:
                return None
        other_sort = other_line.get_sorted_y()
        if self.start[1] < other_sort[0] or self.start[1] > other_sort[1]:
            return None
        return (other_x, self.start[1])
        # same for both

def check_set_neighbours(set_in, coord):
    #item or neighbour in set
    if coord in set_in:
        return coord
    if (coord[0], coord[1]+1) in set_in:
        return (coord[0], coord[1]+1)
    if (coord[0], coord[1]-1) in set_in:
        return (coord[0], coord[1]-1)
    if (coord[0]+1, coord[1]) in set_in:
        return (coord[0]+1, coord[1])
    if (coord[0]-1, coord[1]) in set_in:
        return (coord[0]-1, coord[1])
    return None


class Distances:
    def __init__(self, input):
        self.locations = []
        for inp in input:
            x, y = inp.split(',')
            self.locations.append((int(x), int(y)))

        self.boundaries = [Boundary(self.locations[0], self.locations[1])]
        for i in range(1,len(self.locations)-1):
            self.boundaries.append(Boundary(self.locations[i], self.locations[i+1]))
        self.boundaries.append(Boundary(self.locations[-1], self.locations[0]))

    def get_max_area(self):
        max_area = 0
        for i, loc1 in enumerate(self.locations):
            for loc2 in self.locations[i+1:]:
                max_area = max(max_area, get_area(loc1, loc2))
        return max_area

    def check_boundary(self, boundary):
        intersects = set()
        # print(boundary.start, boundary.end)
        for bound in self.boundaries:
            intersect = bound.intersect(boundary)
            if intersect:
                # print("intersect")
                # print(boundary.start, boundary.end)
                # print(bound.start, bound.end)
                # print(intersect)
                any_neighbour = check_set_neighbours(intersects, intersect)
                if any_neighbour:
                    intersects.discard(any_neighbour)
                else:
                    intersects.add(intersect)
        return len(intersects) != 0


    def get_max_internal(self, loc1, loc2):
        new_boundaries = [
            Boundary(loc1, (loc1[0], loc2[1])),
            Boundary((loc1[0], loc2[1]), loc2),
            Boundary(loc2, (loc2[0], loc1[1])),
            Boundary((loc2[0], loc1[1]), loc1)
        ]
        for boundary in new_boundaries:
            if self.check_boundary(boundary):
                return 0
        # print("survive", loc1, loc2, f"=== {get_area(loc1, loc2)}")
        return get_area(loc1, loc2)

    def get_max_area_in_shape(self):
        max_area = 0
        for i, loc1 in enumerate(self.locations):
            for loc2 in self.locations[i+1:]:
                # print("main--", loc1, loc2, "--main")
                max_area = max(max_area, self.get_max_internal(loc1, loc2))
        return max_area



def main(test: bool=True):
    if test:
        input = test_input.split("\n")
    else:
        input = [x.strip() for x in open("2025/data_9.txt")]

    d = Distances(input)
    print(f"The answer to part 1 is {d.get_max_area()}")
    print(f"The answer to part 2 is {d.get_max_area_in_shape()}")

    # line1 = Boundary((0,100), (0,0))
    # line2 = Boundary((-5, 10), (5, 10))
    # print(line1.intersect(line2))

    # line3 = Boundary((10, 0), (10, 100))
    # print(line1.intersect(line3))

    # line4 = Boundary((10, 10), (5, 10))
    # print(line1.intersect(line4))

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(test=args.test)

print(f"The script took {time() - start:.3f}s")
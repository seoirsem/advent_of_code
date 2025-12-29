import argparse

test_input = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

class SplitterGrid:
    def __init__(self, input):
        self.input = input
        self.lenx = len(input[0])
        self.leny = len(input)
        self.beams = []
        for i, object in enumerate(input[0]):
            if object == "S":
                self.beams.append((i,0))

    def get_at(self, x, y):
        if x < 0 or x >= self.lenx or y < 0 or y >= self.leny:
            return None
        return self.input[y][x]
    
    def step_beams(self):
        splits = 0
        visited = set()
        new_beams = set()
        for beam in self.beams:
            next_step = (beam[0], beam[1]+1)
            if next_step in visited:
                continue
            if self.get_at(*next_step) == ".":
                new_beams.add(next_step)
                visited.add(next_step)
            elif self.get_at(*next_step) == "^":
                visited.add(next_step)
                splits+=1
                new_beams.add((beam[0]-1, beam[1]+1))
                new_beams.add((beam[0]+1, beam[1]+1))
        self.beams = new_beams
        return splits

    def step_all(self):
        total_splits = 0
        for _ in range(self.leny):
            new_splits = self.step_beams()
            total_splits+=new_splits
        return total_splits

def main(test: bool=True):
    if test:
        input = test_input.split("\n")
    else:
        input = [x.strip() for x in open("2025/data_7.txt")]

    grid = SplitterGrid(input)
    print(f"The answer to Part 1 is {grid.step_all()}")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(test=args.test)

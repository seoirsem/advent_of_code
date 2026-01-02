import argparse
from operator import xor
from socket import INADDR_MAX_LOCAL_GROUP
import sqlite3
from time import time
start = time()

test_input = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""

class Input:
    def __init__(self, input) -> None:
        presents = {}
        cur_shape = []
        number = '-1'
        for i, line in enumerate(input):
            if "x" in line:
                break
            if line == "":
                if number == "-1":
                    continue
                else:
                    presents[number] = cur_shape
                    number = "-1"
                    cur_shape = []
                    continue
            if ":" in line:
                number = line[0]
                continue
            cur_shape.append(line)
        self.presents = {}
        for p in presents:
            count_hash = 0
            for line in presents[p]:
                count_hash+=line.count('#')
            self.presents[p] = count_hash

        self.target = []
        for line in input[i:]:
            target, present_vec = line.split(":")
            ta, tb = [int(x) for x in target.split('x')]
            present_vec = [int(x) for x in present_vec.split()]
            self.target.append([(ta, tb), present_vec])

    def check_target(self, size, list):
        size_needed = 0
        for p in self.presents:
            size_needed += self.presents[p]*list[int(p)]

        return size_needed <= size[0]*size[1]

    def check_all(self):
        total = 0
        for target in self.target:
            total+=self.check_target(target[0], target[1])
        return total
            

def main(test: bool=True):
    if test:
        input = test_input.split("\n")
    else:
        input = [x.strip() for x in open("2025/data_12.txt")]

    inp = Input(input)
    print(f"The answer to part 1 is {inp.check_all()}")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(test=args.test)


print(f"The script took {time() - start:.3f}s")
import argparse
from time import time
start = time()
import re
import numpy as np

square = re.compile(r"\[(.*?)\]")
round = re.compile(r"\(([^\[\]()]+)\)")

test_input = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

def add_states(state1, state2):
    state_out = []
    for a, b in zip(state1, state2):
        state_out.append((a+b) % 2)
    return state_out

def add_joltage_states(state1, state2):
    state_out = []
    for a, b in zip(state1, state2):
        state_out.append(a+b)
    return state_out

class Switches:
    def __init__(self, input_line):
        match = re.match(square, input_line).group()[1:-1]
        match = match.replace(".","0").replace("#","1")
        self.target = [int(x) for x in match]
        self.curly = [int(x) for x in input_line.split("{")[1][:-1].split(',')]
        switches = re.findall(round, input_line)
        self.num_targets = len(self.target)
        self.switches = []
        for switch in switches:
            numbers = [int(x) for x in switch.split(',')]
            vector = [0]*self.num_targets
            for num in numbers:
                vector[num] = 1
            self.switches.append(vector)

    
    def try_all(self):
        visited = set()
        states = [[0]*self.num_targets]
        i = 0
        while True:
            i+=1
            new_states = []
            for state in states:
                for switch in self.switches:
                    state_out = add_states(state, switch)
                    if state_out == self.target:
                        return i
                    elif tuple(state_out) in visited:
                        continue
                    else:
                        visited.add(tuple(state_out))
                        new_states.append(state_out)
            states = new_states
    
    def exceeds_requirement(self, state):
        for a, b in zip(self.curly, state):
            if b>a:
                return True
        return False

    def try_all_joltage(self):
        # Brute force no werk...
        min_tar =  
        print(self.curly)
        matrix = np.matrix(self.switches)
        print(matrix)
        # print(np.linalg.inv(matrix))
        # if state_out == self.curly:
        #     return i
            
        return 0

def main(test: bool=True):
    if test:
        input = test_input.split("\n")
    else:
        input = [x.strip() for x in open("2025/data_10.txt")]
    
    total = 0
    total_2 = 0
    for inp in input:
        switch = Switches(inp)
        total += switch.try_all()
        total_2 += switch.try_all_joltage()
    print(f"The answer to part 1 is {total}")
    print(f"The answer to part 2 is {total_2}")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(test=args.test)


print(f"The script took {time() - start:.3f}s")
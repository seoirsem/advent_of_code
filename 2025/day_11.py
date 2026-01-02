import argparse
from time import time
start = time()

test_input = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""

test_input_2 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""

class Connections:

    def __init__(self, input):
        self.connectors = {}
        for line in input:
            this_one, others = line.split(":")
            self.connectors[this_one] = others.split()
        self.rec_save = {}
        self.visited = set()

    def paths_to_end(self, position):
        n_paths = 0
        for path in self.connectors[position]:
            if path == 'out':
                return 1
            n_paths += self.paths_to_end(path)
        return n_paths

    def paths_with_fft(self, position):
        if position in self.rec_save:
            return self.rec_save[position]
        # svr to out, visiting fft and dac
        # need bfs now?
        # no, dfs, but want how many to end with fft, with dac, and with both passed up
        n_paths_fft, n_paths_dac, n_paths_both, n_paths_neither = 0,0,0,0

        for path in self.connectors[position]:
            if path == 'out':
                return 0,0,0,1
            elif path == 'dac':
                p_fft, p_dac, p_b, p_n = self.paths_with_fft('dac')
                n_paths_fft += 0
                n_paths_dac += (p_dac+p_n)
                n_paths_both += (p_fft + p_b)
                n_paths_neither += 0
            elif path == 'fft':
                p_fft, p_dac, p_b, p_n = self.paths_with_fft('fft')
                n_paths_dac += 0
                n_paths_fft += (p_fft+p_n)
                n_paths_both += (p_dac + p_b)
                n_paths_neither += 0
            else:
                r1, r2, r3, r4 = self.paths_with_fft(path)
                n_paths_fft += r1 
                n_paths_dac += r2 
                n_paths_both += r3 
                n_paths_neither += r4
    
        self.rec_save[position] = n_paths_fft, n_paths_dac, n_paths_both, n_paths_neither
        return n_paths_fft, n_paths_dac, n_paths_both, n_paths_neither

    def paths_with_both(self):
        return self.paths_with_fft('svr')[2]


def main(test: bool=True):
    if test:
        input = test_input.split("\n")
    else:
        input = [x.strip() for x in open("2025/data_11.txt")]

    connector = Connections(input)
    print(f"The answer to part 1 is {connector.paths_to_end('you')}")

    if test:
        input = test_input_2.split("\n")
        connector = Connections(input)
    print(f"The answer to part 2 is {connector.paths_with_both()}")
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(test=args.test)


print(f"The script took {time() - start:.3f}s")
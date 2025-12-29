import argparse

test_input = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""

def distance(a, b):
    return sum([(a[i]-b[i])**2 for i in range(3)])
class Locations:

    def __init__(self, input, is_test):
        if is_test:
            number = 10
        else:
            number = 1000
        self.boxes = [[int(y) for y in x.split(",")] for x in input]
        distances = {}
        for i in range(len(self.boxes)):
            for j in range(i+1, len(self.boxes)):
                distances[distance(self.boxes[i], self.boxes[j])] = (i,j)
        distance_vals = list(distances.keys())
        distance_vals.sort()
        lowest_keys = distance_vals[:number]
        self.lowest_pairs = [distances[x] for x in lowest_keys]
        self.all_pairs = [distances[x] for x in distance_vals]
        self.num_boxes = len(input)

    def calculate_circuits(self):
        circuits = []
        for new_pair in self.lowest_pairs:
            combine_idx = []
            new_circuits = []
            for i, circuit in enumerate(circuits):
                not_in = True
                for item in new_pair:
                    if item in circuit:
                        combine_idx.append(i)
                        not_in = False
                        break
                if not_in:
                    new_circuits.append(circuit)
            new_set = set(new_pair)
            for combine in combine_idx:
                new_set.update(circuits[combine])
            new_circuits.append(new_set)
            circuits = new_circuits
        circuit_sizes = [len(x) for x in circuits]
        circuit_sizes.sort()
        return circuit_sizes[-1]*circuit_sizes[-2]*circuit_sizes[-3]

    def calculate_all_circuits(self):
        circuits = []
        for new_pair in self.all_pairs:
            combine_idx = []
            new_circuits = []
            for i, circuit in enumerate(circuits):
                not_in = True
                for item in new_pair:
                    if item in circuit:
                        combine_idx.append(i)
                        not_in = False
                        break
                if not_in:
                    new_circuits.append(circuit)
            new_set = set(new_pair)
            for combine in combine_idx:
                new_set.update(circuits[combine])
            new_circuits.append(new_set)
            circuits = new_circuits
            # print(len(circuits), sum(len(x) for x in circuits))
            if len(circuits) == 1 and len(circuits[0]) == self.num_boxes:
                break
        return self.boxes[new_pair[0]][0]*self.boxes[new_pair[1]][0]



def main(test: bool=True):
    if test:
        input = test_input.split("\n")
    else:
        input = [x.strip() for x in open("2025/data_8.txt")]

    loc = Locations(input, test)
    print(f"The answer to part 1 is {loc.calculate_circuits()}")
    print(f"The answer to part 2 is {loc.calculate_all_circuits()}")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(test=args.test)

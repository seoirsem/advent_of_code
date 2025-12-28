import argparse
from tqdm import tqdm

test_input = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

class Ingredients:
    def __init__(self, input):
        self.fresh = []
        self.ingredients = []
        i = 0
        for i, line in enumerate(input):
            if line == "":
                break
            self.fresh.append([int(x) for x in line.split("-")])
        for line in input[i+1:]:
            self.ingredients.append(int(line))
        # print(self.fresh)
        # print(self.ingredients)

    def count_fresh(self):
        fresh = 0
        for ingredient in self.ingredients:
            is_fresh = False
            for range_in in self.fresh:
                if range_in[0] > ingredient:
                    continue
                elif range_in[1] < ingredient:
                    continue
                else:
                    is_fresh = True
                    break
            fresh += is_fresh
        return fresh
    
    def compare_ranges(self, range1, range2):
        new_ranges = []
        if range2[0] > range1[1] or range2[1] < range1[0]:
            new_ranges.append(range1)
        elif range2[1] >= range1[1] and range2[0] <= range1[0]:
            pass
        elif range2[1] < range1[1] and range2[0] > range1[0]:
            new_ranges.append([range1[0], range2[0]-1])
            new_ranges.append([range2[1]+1,range1[1]])
        elif range1[1] >= range2[0] and range1[0] < range2[0]:
            new_ranges.append([range1[0], range2[0]-1])
        elif range1[0] <= range2[1] and range1[1] > range2[1]:
            new_ranges.append([range2[1]+1, range1[1]])

        return new_ranges


    def count_all(self):
        count = 0    
        for i, range_in in enumerate(self.fresh):
            ranges = [range_in]
            # print("--",ranges)
            for prev_range in self.fresh[0:i]:
                new_ranges = []
                for range in ranges:
                    new_ranges.extend(self.compare_ranges(range, prev_range))
                # print(new_ranges)
                ranges = new_ranges
            # print(sum([x[1]-x[0]+1 for x in ranges]))
            count += sum([x[1]-x[0]+1 for x in ranges])
        return count

def main(test: bool=True):
    if test:
        input = test_input.split("\n")
    else:
        input = [x.strip() for x in open("2025/data_5.txt")]
    ing = Ingredients(input)
    print(f"The answer to part 1 is {ing.count_fresh()}")
    print(f"The answer to part 2 is {ing.count_all()}")
    
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(test=args.test)

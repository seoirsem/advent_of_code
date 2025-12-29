import argparse
from functools import reduce

class Part1:
    def __init__(self, input):
        self.rows = [x.split() for x in input]

    def sums(self):
        total = 0
        for column in zip(*self.rows):
            operator = column[-1]
            if operator == "+":
                total+= sum([int(x) for x in column[:-1]])
            else:
                total += reduce(lambda x,y: int(x)*int(y), column[:-1])

        return total

class Part2:
    def __init__(self, input):
        self.rows = [x.split() for x in input]
        self.operators = []
        self.col_lens = []
        for column in zip(*self.rows):
            self.operators.append(column[-1])
            numbers = column[:-1]
            lengths = [len(x) for x in numbers]
            self.col_lens.append(max(lengths))
        self.biased_rows = [[] for _ in range(len(input[:-1]))]
        total_len = 0
        for col in self.col_lens:
            for j, input_row in enumerate(input[:-1]):
                self.biased_rows[j].append(input_row[total_len:total_len+col])
            total_len+=col+1

    def sums(self):
        total = 0
        for i, numbers in enumerate(zip(*self.biased_rows)):
            operator = self.operators[i]
            new_nums = []
            for place in range(self.col_lens[i]-1, -1, -1):
                n_temp = []
                for number in numbers:
                    if len(number) < self.col_lens[i]:
                        n_temp.append(number + " "*(self.col_lens[i]-len(number)))
                    else:
                        n_temp.append(number)
                numbers = n_temp
                new_num = ""
                for j, num in enumerate(numbers):
                    if num[place] != " ":
                        new_num += num[place]
                new_nums.append(new_num)
            # print(new_nums, operator)
            if operator == "+":
                total+= sum([int(x) for x in new_nums])
            else:
                total += reduce(lambda x,y: int(x)*int(y), new_nums)            
        return total


test_input = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """

def main(test: bool=True):
    if test:
        input = test_input.split("\n")
    else:
        input = [x.strip() for x in open("2025/data_6.txt")]

    p1 = Part1(input)
    print(f"The answer to part 1 is {p1.sums()}")
    p2 = Part2(input)
    print(f"The answer to part 2 is {p2.sums()}")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(test=args.test)

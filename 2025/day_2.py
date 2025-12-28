import argparse
from typing import Iterable

test_input = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"

def parse_input(input: str):
    ranges = []
    for range in input.split(','):
        start, end = range.split("-")
        ranges.append((int(start), int(end)))
    return ranges

def is_invalid(number):
    num_str = str(number)
    length = len(num_str)
    if length%2 == 1:
        return False
    if num_str[0:length//2] == num_str[-length//2:]:
        return True
    return False

def is_invalid_2(number):
    num_str = str(number)
    length = len(num_str)
    if length == 1:
        return False
    for char in num_str:
        if char != num_str[0]:
            break
    else:
        return True

    for i in range(2,length-1):
        if length % i == 0:
            substr = num_str[0:length//i]
            step = length//i
            pos = step
            while pos < length:
                if num_str[pos:pos+step] != substr:
                    break
                pos+=step
            else:
                return True
    return False

def main(test: bool=True):
    input = test_input if test else [x for x in open("2025/data_2.txt")][0]
    ranges = parse_input(input)
    invalid_sum = 0
    invalid_sum_2 = 0
    for r in ranges:
        for x in range(r[0], r[1]+1):
            if is_invalid(x):
                invalid_sum+=x
            if is_invalid_2(x):
                invalid_sum_2+=x
    print(f"The answer to part 1 is {invalid_sum}")
    print(f"The answer to part 2 is {invalid_sum_2}")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(test=args.test)

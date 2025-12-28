import argparse

test_input = """987654321111111
811111111111119
234234234234278
818181911112111"""

def get_joltage(number_str):
    high1, high2 = number_str[-2], number_str[-1]
    number_str_rev = number_str[::-1]
    for char in number_str_rev[2:]:
        if char >= high1:
            if high1 > high2:
                high2 = high1
            high1 = char
    return int(high1+high2)

def check_sub(num_str, new_num):
    if len(num_str) == 1:
        return max(num_str, new_num)
    if new_num >= num_str[0]:
        return new_num + check_sub(num_str[1:], num_str[0])
    else:
        return num_str

def get_joltage2(number_str):
    num_rev = number_str[::-1]
    highstr = number_str[-12:]
    for char in num_rev[12:]:
        highstr = check_sub(highstr, char)
    return int(highstr)

def main(test: bool=True):
    if test:
        input = test_input.split("\n")
    else:
        input = [x for x in open("2025/data_3.txt")]

    total = 0
    total2 = 0
    for bank in input:
        total += get_joltage(bank.strip())
        total2 += get_joltage2(bank.strip())

    print(f"The answer to part 1 is {total}")
    print(f"The answer to part 2 is {total2}")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(test=args.test)

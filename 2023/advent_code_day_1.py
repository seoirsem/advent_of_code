
filename = "input_day_1.txt"

def count_total(filename: str) -> int:
    with open(filename,"r") as file:
        total_sum = 0
        digits = {"0","1","2","3","4","5","6","7","8","9"}
        for line in file:
            d1 = 0
            d2 = 0
            for d in line:
                if d in digits:
                    d1 = d
                    break
            for d in reversed(line):
                if d in digits:
                    d2 = d
                    break
            total_sum += int(d1+d2)
    return total_sum

def count_total_with_strings(filename: str) -> str:
    digits = {"0","1","2","3","4","5","6","7","8","9"}
    numbers = {"zero": "0","one": "1","two": "2","three": "3","four": "4","five": "5","six": "6","seven": "7","eight": "8","nine": "9"}
    def parse_line(line: str, reversed_string: bool) -> str:
        d1 = 0
        length = len(line)
        if reversed_string:
            line = line[::-1]
        for i,d in enumerate(line):
            if d1 != 0:
                break
            if reversed_string:
                substring = line[:i+1]
            else:
                substring = line[:i+1]
            if d in digits:
                d1 = d
                break
            for num in numbers:
                test_substr = substring
                if reversed_string:
                    test_substr = test_substr[::-1]
                if num in test_substr:
                    d1 = numbers[num]
                    break
        return d1

    with open(filename,"r") as file:
        total_sum = 0
        digits = {"0","1","2","3","4","5","6","7","8","9"}
        for line in file:
            d1 = parse_line(line, False)
            d2 = parse_line(line, True)
          
            total_sum += int(d1+d2)
        return total_sum


print(count_total_with_strings(filename))

import re

def sump_mul(string, regex):    
    matching = re.findall(regex,string)
    sum_total = 0
    for (n1,n2) in matching:
        sum_total+= int(n1)*int(n2)
    return sum_total


input_file = "day_3_input.txt"
regex = r"mul\((\d+),(\d+)\)"

with open(input_file,'r') as input:
    string = input.read()

print(f"The answer to part 1 is {sump_mul(string,regex)}")

total_sum = 0
str_do = string.split("do()")#
for sub in str_do:
    sub_dont = sub.split("don't()")
    total_sum+=sump_mul(sub_dont[0],regex)

print(f"The answer to part 2 is {total_sum}")




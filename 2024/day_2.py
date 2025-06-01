
def compare_2(n_low, n_high, increasing):
    if n_low==n_high:
        return False
    if abs(n_low-n_high) > 3:
        return False
    if (n_low - n_high) > 0 and increasing:
        return False
    if (n_low - n_high) < 0 and not increasing:
        return False
    return True


def is_safe(numbers):
    if len(numbers) < 2:
        return True
    if numbers[0] == numbers[1]:
        return False
    increasing = numbers[1]>numbers[0]

    for i in range(len(numbers)-1):
        n_low = numbers[i]
        n_high = numbers[i+1]
        if not compare_2(n_low, n_high, increasing):
            return False
    return True
    

safe_count = 0
input_file = "day_2_input.txt"
with open(input_file,'r') as input:
    for line in input:
        numbers = [int(x) for x in line.rstrip().split()]
        safe_count+=is_safe(numbers)

print(f"The answer to part 1 is {safe_count}")

safe_count = 0
with open(input_file,'r') as input:
    for line in input:
        # print(line, safe_count)
        numbers = [int(x) for x in line.rstrip().split()]
        if is_safe(numbers[1:]) or is_safe(numbers[:-1]):
            safe_count+=1
            continue

        for i in range(1,len(numbers)-1):
            if is_safe(numbers[:i]+numbers[i+1:]):
                safe_count+=1
                break
print(f"The answer to part 2 is {safe_count}")

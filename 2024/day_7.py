
file_in = "day_7_example.txt"
file_in = "day_7_input.txt"

equations = []
with open(file_in,'r') as input:
    for line in input:
        target, numbers = line.rstrip().split(':')
        numbers = [int(x) for x in numbers.split()]
        equations.append((int(target), numbers))


def ternary(n, pad_length):
    if n == 0:
        return '0'*pad_length
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    num_str = ''.join(reversed(nums))
    if len(num_str) < pad_length:
        num_str = "0"*(pad_length-len(num_str)) + num_str
    return num_str

def rec_seq_valid(target, numbers, idx, operators, cache):
    if len(operators) == idx:
        return cache[operators] == target
    if operators[:idx+1] in cache:
        return rec_seq_valid(target, numbers, idx+1, operators,cache)
    operator = operators[idx]
    if idx == 0:
        sum_thus = cache[""]
    else:
        sum_thus = cache[operators[:idx]]
    if operator=="0":
        cache[operators[:idx+1]] = sum_thus+numbers[idx+1]
    elif operator=="1":
        cache[operators[:idx+1]] = sum_thus*numbers[idx+1]
    else:
        cache[operators[:idx+1]] = int(str(sum_thus) + str(numbers[idx+1]))
    return rec_seq_valid(target, numbers, idx+1, operators,cache)

def is_valid(target, numbers, binary):
    cache = {}
    cache[''] = numbers[0]
    if binary:
        for idx in range(2**(len(numbers)-1)):
            operators = f'{idx:0{len(numbers)-1}b}'
            if rec_seq_valid(target, numbers, 0, operators, cache):
                return target
    else:
        for idx in range(3**(len(numbers)-1)):
            operators = ternary(idx, len(numbers)-1)
            if rec_seq_valid(target, numbers, 0, operators, cache):
                return target
    return 0

target_sum = 0
for eq in equations:
    target_sum+=is_valid(*eq, True)
print(f"The answer to part 1 is {target_sum}")

target_sum = 0
for idx, eq in enumerate(equations):
    if idx % 50 == 0:
        print(f"Step: [{idx}/850]")
    target_sum+=is_valid(*eq, False)
print(f"The answer to part 2 is {target_sum}")


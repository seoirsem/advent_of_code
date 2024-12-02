
file_in = "day_1_input.txt"
left_list = []
right_list = []
with open(file_in, 'r') as input:
    for line in input:
        left, right = line.strip().split()
        left_list.append(int(left))
        right_list.append(int(right))

left_list.sort()
right_list.sort()
difference = 0
for left, right in zip(left_list, right_list):
    difference+= abs(left-right)
print(f"The part 1 difference is {difference}")

# left_list = [1,2,3,3,3,4]
# right_list = [3,3,3,4,5,9]
count_sum = 0
index_right = 0
for n in left_list:
    count = 0
    for m in right_list[index_right:]:
        if m == n:
            count+=1
        elif m<n:
            index_right+=1
            continue
        elif m>n:
            break
    count_sum+=count*n

print(f"The part 2 count sum is {count_sum}")

def num_seq_possible(seq: str, word_set,cache):
    if seq in cache:
        return cache[seq]
    num_possible=0
    if seq in word_set:
        num_possible+=1
    for i in range(1,len(seq)):
        if seq[:i] in word_set:
            num_possible += num_seq_possible(seq[i:], word_set, cache)
    cache[seq] = num_possible
    return num_possible


input_file = "2024/inputs/day_19_input.txt"
# input_file = "2024/inputs/day_19_example.txt"

words = []
targets = []
with open(input_file, 'r') as file_in:
    for line in file_in:
        if ',' in line:
            words = line.rstrip().replace(',','').split()
        elif line!="\n":
            targets.append(line.rstrip())

word_set = set(words)

cache = {}
num_possible=0
total_config=0
for t in targets:
    n = num_seq_possible(t,word_set,cache)
    num_possible+=1 if n>0 else 0
    total_config+=n

print(f"The answer to part 1 is {num_possible}")
print(f"The answer to part 2 is {total_config}")



def get_checksum_increase(start_pos, width, id):
    return int(id*(start_pos*width + (width-1)*width/2))

class Gap():
    def __init__(self, start_pos: int, gap_width: int):
        self.start_pos = start_pos
        self.gap_width = gap_width

    def fill_gap(self, width_in: int, id_in: int):
        if width_in == 0:
            return 0, 0, []
        elif self.gap_width==0:
            return 0, width_in, []
        elif width_in <= self.gap_width:
            self.gap_width -= width_in
            delta = width_in
            leftover_in = 0
        else:
            delta = self.gap_width
            leftover_in = width_in - self.gap_width
            self.gap_width = 0

        checksum_increase = get_checksum_increase(self.start_pos, delta, id_in)
        self.start_pos += width_in
        return checksum_increase, leftover_in, [id_in for _ in range(delta)]
    
    def gap_finished(self)-> bool:
        return self.gap_width == 0


def get_sum_to(string_in):
    summ = 0
    for idx, x in enumerate(string_in):
        if x == '.':
            break
        summ+=idx*int(x)
    return summ

input_file = "day_9_input.txt"
# input_file = "day_9_example.txt"

with open(input_file,'r') as input:
    data = input.read().rstrip()
# data = "12345"
idx_start = 0 # where in the array
pos_start = 0 # where in memory
id_start = 0 # what the data id is
# print(len(data))
idx_end = len(data) - 1
id_end = len(data)//2
end_id_carryover_amount = int(data[idx_end])

data_out = []

checksum = 0
while idx_end > idx_start:
    len_seg = int(data[idx_start])
    checksum += get_checksum_increase(pos_start, len_seg, id_start)
    pos_start += len_seg
    data_out+= [id_start for _ in range(len_seg)]

    gap = Gap(pos_start, int(data[idx_start+1]))
    pos_start += gap.gap_width

    if end_id_carryover_amount > 0:
        checksum_inc, end_id_carryover_amount, string = gap.fill_gap(end_id_carryover_amount, id_end)
        data_out+=string
        checksum += checksum_inc

    while not gap.gap_finished():
        idx_end -= 2
        id_end -= 1
        if idx_end < idx_start:
            break
        end_id_carryover_amount = int(data[idx_end])
        checksum_inc, end_id_carryover_amount, string = gap.fill_gap(end_id_carryover_amount, id_end)
        data_out+=string
        checksum+=checksum_inc

    idx_start += 2
    id_start += 1

checksum += get_checksum_increase(pos_start, end_id_carryover_amount, id_end)
data_out+= [id_end for _ in range(end_id_carryover_amount)]


print(f"The answer to part 1 is {checksum}")

id = 0
full_list = []
idx = 0
while idx < len(data):
    for _ in range(int(data[idx])):
        full_list.append(id)

    if idx == len(data)-1:
        break
    for _ in range(int(data[idx+1])):
        full_list.append('.')
    id+=1
    idx+=2

pt_end = len(full_list) - 1
pt_start = 0
while pt_start<pt_end:
    if full_list[pt_start] == '.':
        full_list[pt_start] = full_list[pt_end]
        full_list[pt_end] = '.'
        pt_start += 1
        while full_list[pt_end] == '.':
            pt_end -= 1
    else:
        pt_start +=1

print(f"The answer to part 1 is {get_sum_to(full_list)}")    


id = 0
gaps = [] # start_idx, len
id_locs = [] # start_idx, len, id
idx = 0
position = 0
while idx < len(data):
    data_len = int(data[idx])
    id_locs.append([position, data_len, id])
    if idx == len(data)-1:
        break
    gap_len = int(data[idx+1])
    gaps.append([position+data_len, gap_len])
    position+= (data_len+gap_len)
    id+=1
    idx+=2



checksum = 0
final_locs = []
for i in range(len(id_locs)-1, -1, -1):
    in_gap = False
    start_idx, length, id = id_locs[i]
    for gap in gaps:
        if gap[1] >= length: # gap is big enough
            if gap[0] > start_idx:
                break
            final_locs.append([gap[0], length, id])
            checksum += get_checksum_increase(gap[0], length, id) # start, width, id
            gap[0] += length
            gap[1] -= length
            in_gap = True
            break
    if not in_gap:
        checksum += get_checksum_increase(*id_locs[i])
        final_locs.append(id_locs[i])
        
print(f"The answer to part 2 is {checksum}")

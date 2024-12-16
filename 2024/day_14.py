import re
from functools import reduce
from typing import List
import keyboard, time
 

class Robot():
    def __init__(self, p_x, p_y, v_x, v_y, xlim, ylim):
        self.p_x = int(p_x)
        self.p_y = int(p_y)
        self.v_x = int(v_x)
        self.v_y = int(v_y)
        self.xlim = xlim
        self.ylim = ylim
    
    def take_n_steps(self, n: int):
        x_out = (self.p_x + self.v_x*n) % self.xlim
        y_out = (self.p_y + self.v_y*n) % self.ylim
        return (x_out, y_out)

    def __repr__(self):
        return f"p=({self.p_x},{self.p_y}), v=({self.v_x},{self.v_y})"

example = False
if example:
    input_file = "2024/inputs/day_14_example.txt"
    xlim = 11
    ylim = 7
else:
    input_file = "2024/inputs/day_14_input.txt"
    xlim = 101
    ylim = 103


pos_re = r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)"
robots = []
with open(input_file,'r') as file:
    for line in file:
        robots.append(Robot(*re.findall(pos_re, line)[0], xlim, ylim))

n_steps = 100
end_ps= []
for r in robots:
    end_ps.append(r.take_n_steps(n_steps))

quad_counts = [0,0,0,0]
for px, py in end_ps:
    if px < (xlim-1)/2 and py < (ylim-1)/2:
        quad_counts[0]+=1
    if px > (xlim-1)/2 and py < (ylim-1)/2:
        quad_counts[1]+=1
    if px < (xlim-1)/2 and py > (ylim-1)/2:
        quad_counts[2]+=1
    if px > (xlim-1)/2 and py > (ylim-1)/2:
        quad_counts[3]+=1

print(f"The answer to part 1 is {reduce(lambda a, b: a*b, quad_counts)}")

def poss_after_n(robots: List[Robot], n: int):
    
    for r in robots:
        p_x, p_y = r.take_n_steps(n)
    

def print_after_n(robots: List[Robot], n: int):
    image = [[0 for _ in range(xlim)] for _ in range(ylim)]
    for r in robots:
        p_x, p_y = r.take_n_steps(n)
        image[p_y][p_x] += 1
    for line in image:
        l_out = ""
        for s in line:
            l_out += '.' if s == 0 else str(s)
        print(l_out)




 
button_delay = 0.2
idx = 7861
step = 101
while True:
 
    if keyboard.is_pressed("l"):
        idx+=step
        print_after_n(robots, idx)
        print(f"Second: {idx}, Press Enter to continue...")
        time.sleep(0.1)
    if keyboard.is_pressed("k"):
        idx-=step
        print_after_n(robots, idx)
        print(f"Second: {idx}, Press Enter to continue...")
        time.sleep(0.1)

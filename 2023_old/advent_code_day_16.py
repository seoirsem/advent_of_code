"""
--- Day 16: The Floor Will Be Lava ---
With the beam of light completely focused somewhere, the reindeer leads you deeper still into the Lava Production Facility. At some point, you realize that the steel facility walls have been replaced with cave, and the doorways are just cave, and the floor is cave, and you're pretty sure this is actually just a giant cave.

Finally, as you approach what must be the heart of the mountain, you see a bright light in a cavern up ahead. There, you discover that the beam of light you so carefully focused is emerging from the cavern wall closest to the facility and pouring all of its energy into a contraption on the opposite side.

Upon closer inspection, the contraption appears to be a flat, two-dimensional square grid containing empty space (.), mirrors (/ and \), and splitters (| and -).

The contraption is aligned so that most of the beam bounces around the grid, but each tile on the grid converts some of the beam's light into heat to melt the rock in the cavern.

You note the layout of the contraption (your puzzle input). For example:

.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
The beam enters in the top-left corner from the left and heading to the right. Then, its behavior depends on what it encounters as it moves:

If the beam encounters empty space (.), it continues in the same direction.
If the beam encounters a mirror (/ or \), the beam is reflected 90 degrees depending on the angle of the mirror. For instance, a rightward-moving beam that encounters a / mirror would continue upward in the mirror's column, while a rightward-moving beam that encounters a \ mirror would continue downward from the mirror's column.
If the beam encounters the pointy end of a splitter (| or -), the beam passes through the splitter as if the splitter were empty space. For instance, a rightward-moving beam that encounters a - splitter would continue in the same direction.
If the beam encounters the flat side of a splitter (| or -), the beam is split into two beams going in each of the two directions the splitter's pointy ends are pointing. For instance, a rightward-moving beam that encounters a | splitter would split into two beams: one that continues upward from the splitter's column and one that continues downward from the splitter's column.
Beams do not interact with other beams; a tile can have many beams passing through it at the same time. A tile is energized if that tile has at least one beam pass through it, reflect in it, or split in it.

In the above example, here is how the beam of light bounces around the contraption:

>|<<<\....
|v-.\^....
.v...|->>>
.v...v^.|.
.v...v^...
.v...v^..\
.v../2\\..
<->-/vv|..
.|<<<2-|.\
.v//.|.v..
Beams are only shown on empty tiles; arrows indicate the direction of the beams. If a tile contains beams moving in multiple directions, the number of distinct directions is shown instead. Here is the same diagram but instead only showing whether a tile is energized (#) or not (.):

######....
.#...#....
.#...#####
.#...##...
.#...##...
.#...##...
.#..####..
########..
.#######..
.#...#.#..
Ultimately, in this example, 46 tiles become energized.

The light isn't energizing enough tiles to produce lava; to debug the contraption, you need to start by analyzing the current situation. With the beam starting in the top-left heading right, how many tiles end up being energized?

-- Part Two ---
As you try to work out what might be wrong, the reindeer tugs on your shirt and leads you to a nearby control panel. There, a collection of buttons lets you align the contraption so that the beam enters from any edge tile and heading away from that edge. (You can choose either of two directions for the beam if it starts on a corner; for instance, if the beam starts in the bottom-right corner, it can start heading either left or upward.)

So, the beam could start on any tile in the top row (heading downward), any tile in the bottom row (heading upward), any tile in the leftmost column (heading right), or any tile in the rightmost column (heading left). To produce lava, you need to find the configuration that energizes as many tiles as possible.

In the above example, this can be achieved by starting the beam in the fourth tile from the left in the top row:

.|<2<\....
|v-v\^....
.v.v.|->>>
.v.v.v^.|.
.v.v.v^...
.v.v.v^..\
.v.v/2\\..
<-2-/vv|..
.|<<<2-|.\
.v//.|.v..
Using this configuration, 51 tiles are energized:

.#####....
.#.#.#....
.#.#.#####
.#.#.##...
.#.#.##...
.#.#.##...
.#.#####..
########..
.#######..
.#...#.#..
Find the initial beam configuration that energizes the largest number of tiles; how many tiles are energized in that configuration?

"""



def print_grid(arr: list[list[str]])-> None:
    max_width = max(len(str(item)) for row in arr for item in row)
    formatted_grid = "\n".join(" ".join(f"{str(item):<{max_width}}" for item in row) for row in arr)
    print(formatted_grid)

def next_position(ray: ((int,int),(int,int))) -> ((int,int),(int,int)):
    return ((ray[0][0]+ray[1][0],ray[0][1]+ray[1][1]),(ray[1][0],ray[1][1]))
    
def check_on_screen(ray: ((int,int),(int,int)))-> bool:
    """
    checks whether the current point OR the next point are invalid
    """
    (i,j) = ray[0]
    #print(i,j)
    if i<0 or i>WIDTH-1:
        return False
    elif j<0 or j>HEIGHT-1:
        return False
    # elif i+u<0 or i+u>WIDTH-1:
    #     return False
    # elif j+v<0 or j+v>HEIGHT-1:
    #     return False
    else:
        return True

def rotate_velocity(vel: (int,int), char: str)-> (int,int):
    v_2 = (0,0)
    if char == "/":
        v_2 = (vel[1]*-1,vel[0]*-1)
    elif char == "\\":
        v_2 = (vel[1],vel[0])
    return v_2

def follow_ray(ray: ((int,int),(int,int)), array: list[str])-> list:
    new_rays = []

    while True:
        if not check_on_screen(ray):
            break
        if ray in visit_velocity_set:
            break
        else:
            visit_velocity_set.add(ray)
        visited_set.add(ray[0])

        c = array[ray[0][1]][ray[0][0]]
        if c == ".":
            ray = next_position(ray)
        elif c == "|":
            if ray[1][1] == 0:
                new_ray = next_position((ray[0],(0,1)))
                new_rays.append(new_ray)
                ray = next_position((ray[0],(0,-1)))
            else:
                ray = next_position(ray)
        elif c == "-":
            if ray[1][0] == 0:
                new_ray = next_position((ray[0],(1,0)))
                new_rays.append(new_ray)
                ray = next_position((ray[0],(-1,0)))                
            else:
                ray = next_position(ray)
        elif c == "/" or c == "\\":
            ray = next_position((ray[0],rotate_velocity(ray[1],c)))

    return new_rays

filename = "test_input_day_16.txt"
filename = "input_day_16.txt"

array = []
with open(filename,"r") as file:
    for line in file:
        array.append(line)
        #print(line)


WIDTH = len(array[0])-1
HEIGHT = len(array)

visited_set = set()
visit_velocity_set = set()# (position, velocity) - removes overlaps of paths (e.g loops)
ray_list = []
ray_list.append(((0,0),(1,0)))# (position, velocity)

while len(ray_list)>0:
    new_rays = follow_ray(ray_list.pop(0),array)
    if new_rays is not []:
        ray_list.extend(new_rays)

print(f"The grid has dimensions ({WIDTH},{HEIGHT})")
for v in visited_set:
    if v[0] >= 110 or v[1] >= 110:
        print(v)

print(f"P1: {len(visited_set)} cells are energised")

array_list = []
for line in array:
    line2 = []
    for c in line:
        if c != "\n":
            line2.append(c)
    line2.append("\n")
    array_list.append(line2)

for v in visited_set:
    array_list[v[1]][v[0]] = "#"

# if True:
#     filename = "advent_code_day_16_out.txt"
#     with open(filename,"w") as file:
#         for line in array_list:
#             file.write("".join(line))

#print_grid(array_list)
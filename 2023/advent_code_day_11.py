"""
--- Day 11: Cosmic Expansion ---
You continue following signs for "Hot Springs" and eventually come across an observatory. The Elf within turns out to be a researcher studying cosmic expansion using the giant telescope here.

He doesn't know anything about the missing machine parts; he's only visiting for this research project. However, he confirms that the hot springs are the next-closest area likely to have people; he'll even take you straight there once he's done with today's observation analysis.

Maybe you can help him with the analysis to speed things up?

The researcher has collected a bunch of data and compiled the data into a single giant image (your puzzle input). The image includes empty space (.) and galaxies (#). For example:

...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies. However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the observatory.

Due to something involving gravitational effects, only some space expands. In fact, the result is that any rows or columns that contain no galaxies should all actually be twice as big.

In the above example, three columns and two rows contain no galaxies:

   v  v  v
 ...#......
 .......#..
 #.........
>..........<
 ......#...
 .#........
 .........#
>..........<
 .......#..
 #...#.....
   ^  ^  ^
These rows and columns need to be twice as big; the result of cosmic expansion therefore looks like this:

....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......
Equipped with this expanded universe, the shortest path between every pair of galaxies can be found. It can help to assign every galaxy a unique number:

....1........
.........2...
3............
.............
.............
........4....
.5...........
............6
.............
.............
.........7...
8....9.......
In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't matter. For each pair, find any shortest path between the two galaxies using only steps that move up, down, left, or right exactly one . or # at a time. (The shortest path between two galaxies is allowed to pass through another galaxy.)

For example, here is one of the shortest paths between galaxies 5 and 9:

....1........
.........2...
3............
.............
.............
........4....
.5...........
.##.........6
..##.........
...##........
....##...7...
8....9.......
This path has length 9 because it takes a minimum of nine steps to get from galaxy 5 to galaxy 9 (the eight locations marked # plus the step onto galaxy 9 itself). Here are some other example shortest path lengths:

Between galaxy 1 and galaxy 7: 15
Between galaxy 3 and galaxy 6: 17
Between galaxy 8 and galaxy 9: 5
In this example, after expanding the universe, the sum of the shortest path between all 36 pairs of galaxies is 374.

Expand the universe, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?

--- Part Two ---
The galaxies are much older (and thus much farther apart) than the researcher initially estimated.

Now, instead of the expansion you did before, make each empty row or column one million times larger. That is, each empty row should be replaced with 1000000 empty rows, and each empty column should be replaced with 1000000 empty columns.

(In the example above, if each empty row or column were merely 10 times larger, the sum of the shortest paths between every pair of galaxies would be 1030. If each empty row or column were merely 100 times larger, the sum of the shortest paths between every pair of galaxies would be 8410. However, your universe will need to expand far beyond these values.)

Starting with the same initial image, expand the universe according to these new rules, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?

"""

import re

def calculate_length_sum(filename: str, expansion_constant: int = 2)-> int:

    file_list = []
    WIDTH = 0
    HEIGHT = 0
    with open(filename,"r") as file:
        line = next(file)
        #print(line)
        WIDTH = len(line) - 1 #subtract 1 for the newline character
        file_list.append(re.finditer("#",line))
        for line in file:   
            #print(line)
            file_list.append(re.finditer("#",line))
    HEIGHT = len(file_list)

    print(f"The galaxy has dimensions ({WIDTH},{HEIGHT})")
    width_set = set(range(WIDTH))
    height_set = set(range(HEIGHT))

    points = []
    for i, line in enumerate(file_list):
        for star in line:
            j = star.span()[0]
            points.append((i,j))

    for (i,j) in points:
        if i in height_set:
            height_set.remove(i)
        if j in width_set:
            width_set.remove(j)

    sum_to_width = {}
    sum_to_width[0] = 0 # we dont care if the zero term expands as we only look at differences later
    for j in range(1,WIDTH):
        if j in width_set:
            sum_to_width[j] = sum_to_width[j-1]+expansion_constant
        else:
            sum_to_width[j] = sum_to_width[j-1]+1

    sum_to_height = {}
    sum_to_height[0] = 0 # we dont care if the zero term expands as we only look at differences later
    for i in range(1,HEIGHT):
        if i in height_set:
            sum_to_height[i] = sum_to_height[i-1]+expansion_constant
        else:
            sum_to_height[i] = sum_to_height[i-1]+1

    #print(points)
    #print(sum_to_height)
    print(f"The expanded galaxy has dimensions ({sum_to_width[WIDTH-1]},{sum_to_height[HEIGHT-1]})")

    total_distance = 0
    for n,p1 in enumerate(points[:-1]):
        for m in range(n+1,len(points)):
            p2 = points[m]
            total_distance += abs(sum_to_height[p1[0]]-sum_to_height[p2[0]]) + abs(sum_to_width[p1[1]]-sum_to_width[p2[1]])
            #print(f"({n+1}->{m+1})",sum_to_height[p1[0]],sum_to_height[p2[0]],sum_to_width[p1[1]],sum_to_width[p2[1]],abs(sum_to_height[p1[0]]-sum_to_height[p2[0]]) + abs(sum_to_width[p1[1]]-sum_to_width[p2[1]]))
            #print(p1,p2)
    #        print(p1,p2,abs(sum_to_height[p1[1]]-sum_to_height[p2[1]]) + abs(sum_to_width[p1[0]]-sum_to_width[p2[0]]))
    return total_distance

def main():
    
    filename = "test_input_day_11.txt"
    filename = "input_day_11.txt"
    print("###### P1 ######")
    print(f"P1: The total distance between galaxies is {calculate_length_sum(filename)}")
    print("###### P1 ######")
    print(f"P2: The total distance between galaxies is {calculate_length_sum(filename,1000000)}")

if __name__ == "__main__":
    main()
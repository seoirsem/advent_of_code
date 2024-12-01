"""
--- Day 3: Gear Ratios ---
You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?

--- Part Two ---
The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?
"""

import numpy as np
import re

def search_surr_for_symbol(bool_array: np.array, location: (int,int)) -> bool:
    x_range = location[0]
    y_range = location[1]

    if location[0] > 0 and location[0] < X_EXTENT - 1:
        x_range = range(location[0] - 1, location[0] + 1 + 1)
    elif location[0] == 0:
        x_range = range(location[0], location[0] + 1 + 1)
    elif location[0] == X_EXTENT - 1:
        x_range = range(location[0] - 1, location[0] + 1)
    if location[1] > 0 and location[1] < Y_EXTENT - 1:
        y_range = range(location[1] - 1, location[1] + 1 + 1)
    elif location[1] == 0:
        y_range = range(location[1], location[1] + 1 + 1)
    elif location[1] == Y_EXTENT - 1:
        y_range = range(location[1] - 1, location[1] + 1)
    
    for x in x_range:
        for y in y_range:
            #print((x,y), bool_array[x,y])
            if bool_array[x,y] == 1:
                return True
    return False

def check_number_string(bool_array: np.array, locations: list[(int,int)] ) -> bool:
    for location in locations:
        if search_surr_for_symbol(bool_array, location):
            return True
    return False

def create_symbol_array(filename: str) -> np.array:
    bool_array = np.zeros((X_EXTENT,Y_EXTENT))
    with open(filename,"r") as file:
        for i, line in enumerate(file):
            for j, c in enumerate(line[:-1]):
                if c not in characters:
                    bool_array[i,j] = 1
    return bool_array

# (i,j) is (row_number, column_number)
X_EXTENT = 140
Y_EXTENT = 140
characters = {"0","1","2","3","4","5","6","7","8","9","."}
numbers = {"0","1","2","3","4","5","6","7","8","9"}

def question_part_1(filename: str) -> int:
    bool_array = create_symbol_array(filename)
    part_number_sum = 0
    with open(filename,"r") as file:
        for i, line in enumerate(file):
            j = 0
            while j < Y_EXTENT:
                locations = []
                digits = ""
                if line[j] in numbers:
                    locations.append((i,j))
                    digits += line[j]
                    if j != Y_EXTENT - 1:
                        k = j+1
                        #print(line[k])
                        while line[k] in numbers:
                            locations.append((i,k))
                            digits += line[k]
                            k+=1
                        j = k
                    if check_number_string(bool_array, locations):
                        part_number_sum += int(digits)
                j+=1

    print(f"P1: The sum of all the valid part numbers is {part_number_sum}")

def range_overlap(location: (int,int), span: (int,int)) -> bool:
    if span[0] >= location[1] - 1 and span[0] <= location[1] + 1:
        #print(location,span,"1")
        return True
    elif span[1] >= location[1] and span[1] <= location[1] + 1:
        #print(location,span,"2")
        return True
    else:
        return False

def find_surrounding_numbers(lines: list[str], location: (int,int)) -> list[int]:

    if location[0] == 0:
        row_range = range(0,1)
    elif location[0] == X_EXTENT:
        row_range = range(X_EXTENT-1,X_EXTENT+1)
    else:
        row_range = range(location[0]-1,location[0]+2)
    overlaps = []

    for row in row_range:
        for match in search_line(lines[row]):
            if range_overlap(location, match.span()):
                overlaps.append(match.group())
    
    return overlaps

def search_line(line: str) -> list[int]:
    num_regex = r"\d+"   
    return re.finditer(num_regex,line)

#    print([ind.span for ind in indices])


def question_part_2(filename):
    lines = []
    with open(filename,"r") as file:
        for line in file:
            lines.append(line)
    gear_sum = 0
    for i, line in enumerate(lines):
        stars = re.finditer(r"\*",line)
        for star in stars:
            bordering_numbers = find_surrounding_numbers(lines,(i,star.span()[0]))
            #print(bordering_numbers)
            if len(bordering_numbers) == 2:
                gear_sum += int(bordering_numbers[0])*int(bordering_numbers[1])
    print(f"P2: The sum of the gear products is {gear_sum}")
    return gear_sum
    

def main():
    filename = "input_day_3.txt"
    pt_1_answer = question_part_1(filename)
    pt_2_answer = question_part_2(filename)


if __name__ == "__main__":
    main()


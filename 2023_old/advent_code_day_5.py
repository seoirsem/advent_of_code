"""
--- Day 5: If You Give A Seed A Fertilizer ---
You take the boat and find the gardener right where you were told he would be: managing a giant "garden" that looks more to you like a farm.

"A water source? Island Island is the water source!" You point out that Snow Island isn't receiving any water.

"Oh, we had to stop the water because we ran out of sand to filter it with! Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand soon; we only turned off the water a few days... weeks... oh no." His face sinks into a look of horrified realization.

"I've been so busy making sure everyone here has food that I completely forgot to check why we stopped getting more sand! There's a ferry leaving soon that is headed over in that direction - it's much faster than your boat. Could you please go check it out?"

You barely have time to agree to this request when he brings up another. "While you wait for the ferry, maybe you can help us with our food production problem. The latest Island Island Almanac just arrived and we're having trouble making sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:

seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert a seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by one, the maps describe entire ranges of numbers that can be converted. Each line within a map contains three numbers: the destination range start, the source range start, and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48
The first line has a destination range start of 50, a source range start of 98, and a range length of 2. This line means that the source range starts at 98 and contains two values: 98 and 99. The destination range is the same length, but it starts at 50, so its two values are 50 and 51. With this information, you know that seed number 98 corresponds to soil number 50 and that seed number 99 corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51
With this map, you can look up the soil number required for each initial seed number:

Seed number 79 corresponds to soil number 81.
Seed number 14 corresponds to soil number 14.
Seed number 55 corresponds to soil number 57.
Seed number 13 corresponds to soil number 13.
The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do this, you'll need to convert each seed number through other categories until you can find its corresponding location number. In this example, the corresponding types are:

Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?

Your puzzle answer was 825516882

- Part Two ---
Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13
This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?
"""


import re
from typing import Dict, Generator
from math import inf, floor

def range_text_to_map(range_text: str)-> list[int]:
    return [int(x) for x in re.findall(r"\d+", range_text)]

def return_map_list(file : Generator, map_list: list[list[int]]) -> list[list[int]]:

    while True:
        try:
            line = range_text_to_map(next(file))
        except StopIteration:
            break
        if line != []:
            map_list.append(line)
        else:
            break
    return file, map_list

def minimum_seed(seeds: list[int], maps: list[list[int]]) -> int:
    minimum_location = inf
    minimum_seed = 0
    for seed in seeds:
        index = seed
        for map_lists in maps:
            for single_map in map_lists:
                # if there are no matches, index just stays the same
                if index >= single_map[1] and index <= single_map[1] + single_map[2]:
                    index = single_map[0] - single_map[1] + index
                    break
        if minimum_location>index:
            minimum_location = min(minimum_location,index)
            minimum_seed = seed
        print(f"{seed} maps to location {index}")


    print(f"P1: The minimum location is to start with seed {minimum_seed} which maps to location {minimum_location}")
    return minimum_location

def single_ranges_overlap(seed_range: list[int], map_range: list[int])-> list[list[int]]:
    #everything is returned in seed (input) space
    overlap = [[],[]] # [overlap, extra]
    seed_start = seed_range[0]
    seed_end = seed_range[1]
    map_start = map_range[1]
    map_end = map_range[1] + map_range[2]
    #print(seed_start,seed_end,map_start,map_end)
    if seed_end < map_start:
        overlap[1] = seed_range
    elif seed_start > map_end:
        overlap[1] = seed_range
    elif seed_start >= map_start and seed_end <= map_end:
        overlap[0] = seed_range
    elif seed_start < map_start and seed_end > map_end:
        overlap[0] = [map_start, map_end]
        overlap[1] = [[seed_start,map_start-1], [map_end+1, seed_end]]
    elif seed_start < map_start:
        overlap[0] = [map_start,seed_end]
        overlap[1] = [[seed_start, map_start-1]]
    elif seed_end > map_end:
        overlap[0] = [seed_start, map_end]
        overlap[1] = [[map_end+1, seed_end]]

    return overlap

def map_given_overlap(map_range: list[int], overlap: list[int])-> list[int]:
    new_range = []
    new_range.append((overlap[0] - map_range[1]) + map_range[0])
    new_range.append((overlap[1] - map_range[1]) + map_range[0])
    return new_range

def single_seed_range_mapping(seed_range: list[int], map_ranges: list[list[int]])-> list[list[int]]:
    new_ranges = []
    out_of_overlap = [seed_range]
    for map_range in map_ranges:
        new_out_of_overlap = []
        for out_range in out_of_overlap:
            [overlap, not_overlap] = single_ranges_overlap(seed_range, map_range)
            if overlap == []:
                new_out_of_overlap.append(out_range)
            else:
                for x in not_overlap:
                    new_out_of_overlap.append(x)
                new_ranges.append(map_given_overlap(map_range, overlap))
        out_of_overlap = new_out_of_overlap

    if out_of_overlap != []:
        for x in out_of_overlap:
            new_ranges.append(x)
    print(new_ranges)
    return new_ranges



def seed_range_to_location_range(seed_range: list[int], maps: list[list[int]]) -> list[int]:
    indices = [seed_range]
 #   print(indices)
    for map_lists in maps:
        new_indices = []
        for index in indices:
            for x in single_seed_range_mapping(index, map_lists):
                new_indices.append(x)
        indices = new_indices
#        print(indices)
    return indices

def part_1(seeds: list[int], maps: list[list[int]] ) -> int:
    print(f"The starter seeds are {seeds}")
    return minimum_seed(seeds, maps)

   
def part_2(seeds: list[int], maps: list[list[int]] ) -> int:
    minimum_location = inf

    for i in range (floor(len(seeds)/2)):
        seed_range = [seeds[2*i],seeds[2*i]+ seeds[2*i+1]]
        print(seed_range)
        location_ranges = seed_range_to_location_range(seed_range,maps)
        #print(location_ranges)
        for location_range in location_ranges:
            if location_range[0] < minimum_location and location_range[0] !=0:
                minimum_location = location_range[0]
        
    print(f"P2: The minimum location is {minimum_location}")
    return minimum_location


def main():

    filename = "input_day_5.txt"
    seeds = []
    maps = []
    #  we just check for a colon in the line
    re_inputted = re.compile(r"\:(.*)")
    with open(filename,"r") as file:
        seeds = [int(x) for x in re.findall(r"\d+",re.search(re_inputted, next(file)).group())]
        for line in file:
            if re.search(re_inputted, line) is not None:
                file, map1 = return_map_list(file, [])
                maps.append(map1)
                #print(map1)

    minimum_number_1 = part_1(seeds, maps)
    minimum_number_2 = part_2(seeds, maps)
if __name__ == "__main__":
    main()
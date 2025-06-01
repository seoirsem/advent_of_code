from dataclasses import dataclass
from typing import List
from collections import defaultdict

@dataclass
class Coordinate():
    x: int
    y: int

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Coordinate(x,y)

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            return NotImplemented
        return Coordinate(self.x*other, self.y*other)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False
    
    def rot_90(self):
        x = self.x
        self.x = -self.y
        self.y = x
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def flipped(self):
        return Coordinate(-self.x, -self.y)

class Room():
    def __init__(self, data: List[str]):
        self.data = data
        self.xlim = len(data[0])
        self.ylim = len(data)
    
    def get_coord(self, pt: Coordinate):
        x = pt.x
        y = pt.y
        if x < 0 or x >= self.xlim or y < 0 or y >= self.ylim:
            return None
        return self.data[y][x]

    def get_pos_in_line(self, start_pos: Coordinate, dir: Coordinate):
        pos = []
        cur_pos = start_pos
        coord = self.get_coord(start_pos)
        while coord in [".","^"]:
            pos.append(cur_pos)
            cur_pos = cur_pos + dir
            coord = self.get_coord(cur_pos)
        return pos

def hashable_pos_dir(position: Coordinate, direction: Coordinate):
    return (position.x, position.y, direction.x, direction.y)

def forward_search(room: Room, start_pos: Coordinate, dir_in: Coordinate, start_hash: Coordinate, already_seen):
    dir = Coordinate(dir_in.x, dir_in.y)
    pos = Coordinate(start_pos.x, start_pos.y)
    dir.rot_90()
    visited_local = set()
    while True:
        hash_loc = hashable_pos_dir(pos,dir)
        if hash_loc in already_seen or hash_loc in visited_local:
            return start_hash
        else:
            visited_local.add(hash_loc)
        new_pos = pos+dir
        next_tile = room.get_coord(new_pos)
        if next_tile == "#" or new_pos==start_hash:
            dir.rot_90()
        elif next_tile == "." or next_tile == "^":
            pos = new_pos
        else:
            break
    return False

input_file = "day_6_input.txt"
# input_file = "day_6_example.txt"

room_lines = []
with open(input_file,'r') as input:
    for idx, line in enumerate(input):
        if '^' in line:
            guard_pos = Coordinate(line.index("^"),idx)
            guard_dir = Coordinate(0, -1)
        room_lines.append(line.rstrip())

starting_pos = Coordinate(guard_pos.x, guard_pos.y)
room = Room(room_lines)
visited_dir = set()
barrier_locs = set()
# dont try barriers on the path
visited =set()
while True:
    if len(visited) % 500 == 0:
        print(len(visited))
    visited.add(guard_pos)
    visited_dir.add(hashable_pos_dir(guard_pos, guard_dir))
    next_pos = guard_pos+guard_dir
    next_tile = room.get_coord(next_pos)
    if next_tile == "." or next_tile == "^":
        start_hash = guard_pos + guard_dir
        if start_hash not in barrier_locs and start_hash not in visited:
            barrier_loc = forward_search(room, guard_pos, guard_dir, start_hash, visited_dir)
            if barrier_loc and barrier_loc!=starting_pos:
                barrier_locs.add(start_hash)
        guard_pos = next_pos
    elif next_tile == "#":
        guard_dir.rot_90()
    else:
        break


print(f"The answer to part 1 is {len(visited)}")
print(f"The answer to part 2 is {len(barrier_locs)}")


class Tile():
    def __init__(self, id, lines: list[str]):
        self.id = id
        

input_file = "day_20_input.txt"
input_file = "day_20_example.txt"

with open(input_file,'r') as input:
    for line in input:
        if "Tile" in line:
            id = int(line.split()[1][:-1])
            print(id)
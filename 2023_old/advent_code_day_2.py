
filename = "input_day_2.txt"

totals = {"red": 12, "green": 13, "blue": 14}

with open(filename,"r") as file:
    index_sum = 0
    for line in file:
        line_ok = True
        index_string, games = line.split(':')
        index = int(index_string.split(' ')[1])

        games = games[:-1].split(";")
        for game in games:
            if not line_ok:
                break
            balls = game.split(',')
            for ball in balls:
                number, colour = ball[1:].split(" ")
                number = int(number)
                if number > totals[colour]:
                    line_ok = False
                #print(line_ok, colour, number)
        if line_ok:
            index_sum += index
print(index_sum)


with open(filename,"r") as file:
    power_sum = 0
    for line in file:
        minimum = {"red": 0, "green": 0, "blue": 0}

        index_string, games = line.split(':')
        index = int(index_string.split(' ')[1])

        games = games[:-1].split(";")
        for game in games:
            balls = game.split(',')
            for ball in balls:
                number, colour = ball[1:].split(" ")
                minimum[colour] = max(minimum[colour],int(number))

        power = minimum["red"]*minimum["green"]*minimum["blue"]
                #print(line_ok, colour, number)
        power_sum+=power
#        print(line, power)

print(power_sum)
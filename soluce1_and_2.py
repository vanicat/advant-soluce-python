#%%

with open("input") as input:
    text = input.readlines()

#%%
result = 0
for line in text:
    line = [x for x in line if x.isdigit()]
    result += int((line[0] + line[-1]))

print(result)
# %%

import re
digit = [
    "one", "two", "three", "four", "five", "six", "seven",
    "eight", "nine", "[0-9]"
]
convert = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9, 
}
for i in range(10):
    convert[str(i)] = i
print(convert)

print("|".join(digit))
regex = re.compile("|".join(digit))


def day1():
    result = 0
    for line in text:
        first_digit = regex.search(line)
        fd = line[first_digit.start():first_digit.end()]
        digit = first_digit
        while digit:
            last_digit = line[digit.start():digit.end()]
            digit = regex.search(line, digit.start()+1)

        value = 10 * convert[fd] + convert[last_digit]
        result += value
    print(result)

# %%

with open("input-day2.txt") as input:
    text = input.readlines()

def read_game(line):
    line = line.strip()
    game, tirage = line.split(': ')
    id_game = int(game[4:])
    games = []
    for tirage in [ti.split(', ') for ti in tirage.split('; ')]:
        tirage = [ti.split(' ') for ti in tirage]
        games.append({
            color: int(nombre)
            for nombre, color in tirage
        })

    return id_game, games

def test_game(game):
    for tirage in g:
        if tirage.get('red', 0) > 12:
            return False
        if tirage.get('blue', 0) > 14:
            return False
        if tirage.get('green', 0) > 13:
            return False
        if set(iter(tirage)).difference(set(['red', 'blue', 'green'])):
            return False
    return True

def day2_part1():
    result = 0
    for line in text:
        id, g = read_game(line)
        if test_game(g):
            result += id

    return(result)

def puissance(game):
    blue = max([t.get("blue",0) for t in game])
    red = max([t.get("red", 0) for t in game])
    green = max([t.get("green", 0) for t in game])

    return blue * red * green
  

def day2_part2():
    result = 0
    for line in text:
        id, g = read_game(line)
        result += puissance(g)

    return(result)

print(day2_part2())


# %%

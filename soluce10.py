#%% 
from functools import reduce
import io
from typing import Any, Generator, Literal
#%%

Direction =  Literal["N", "S", "W", "E"]
all_direction:list[Direction] = ["N", "S", "W", "E"]


test_input = io.StringIO("""..F7.
.FJ|.
SJ.L7
|F--J
LJ...
""")

def read_data(input:io.TextIOBase) -> list[list[str]]:
    lines = input.readlines()
    lines.insert(0, "." * len(lines[0]))
    lines.append("." * len(lines[0]))
    return [list("." + s + ".") for s in lines]

test_data = read_data(test_input)

direction_case = {
    "F":("S", "E"),
    "|":("S", "N"),
    "-":("W", "E"),
    "J":("N", "W"),
    "7":("S", "W"),
    "L":("N", "E"),
    ".":()
}

opose = {
    "N": "S",
    "S": "N",
    "W": "E",
    "E": "W",
}

direction_move = {
}
for pos, dirs in direction_case.items():
    if len(dirs) == 2:
        d1, d2 = dirs
        direction_move[(pos, opose[d1])] = d2
        direction_move[(pos, opose[d2])] = d1

#%%

def move(x:int, y:int, direction:Direction):
    match direction:
        case "N":
            return (x, y-1)
        case "S":
            return (x, y+1)
        case "E":
            return (x+1, y)
        case "W":
            return (x-1, y)
        case _:
            assert False

def find_start(data:list[list[str]]) -> tuple[int, int]:
    for i, line in enumerate(data):
        for j, c in enumerate(line):
            if c == "S":
                return (j, i)
    assert False

test_x, test_y = find_start(test_data)
print(test_x, test_y)

def find_first_dir(data:list[list[str]], x:int, y:int) -> Generator[Direction, Any, Any]:
    for dir in all_direction:
        nx, ny = move(x, y, dir)
        place = data[ny][nx]
        if opose[dir] in direction_case[place]:
            yield dir

print(find_first_dir(test_data, test_x, test_y))

def duplicate(data):
    return [ [ "." for _ in line] for line in data ]


def find_cycle(data):
    plan = duplicate(data)

    start_x, start_y = find_start(data)
    dir, dir2 = find_first_dir(data, start_x, start_y)

    for form, dirs in direction_case.items():
        if { dir, dir2 } == set(dirs):
            plan[start_y][start_x] = form 

    x, y = move(start_x, start_y, dir)
    dir = direction_move[data[y][x], dir]
    step = 1
    while True:
        plan[y][x] = data[y][x]
        x, y = move(x, y, dir)
        step += 1
        if data[y][x] == "S":
            return step // 2, plan
        dir = direction_move[data[y][x], dir]

find_cycle(test_data)


# %%

with open("input-day10.txt") as f:
    data = read_data(f)

find_cycle(data)
# %%

values = {
    ".": 0,
    "|": 1,
    "-": 0,
    "L": 0.5,
    "J": -0.5,
    "7": 0.5,
    "F": -0.5,
}

def test_a_stuff(data):
    data = read_data(io.StringIO(data))
    plan, enclosed = enclose(data)

    for line in plan:
        print("".join(line))

    return plan

def enclose(data):
    score, plan = find_cycle(data)

    enclosed = 0
    for line in plan:
        place = 0
        for i, elem in enumerate(line):
            if elem == ".":
                if place % 2 == 1:
                    line[i] = "I"
                    enclosed += 1
                else:
                    line[i] = "O"
            else:
                place += values[elem]
    return plan,enclosed

test_a_stuff(
    """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""
)


print()

test_a_stuff("""FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""")    
# %%

enclose(data)
# %%

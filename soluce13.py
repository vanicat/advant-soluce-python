#%%

import io
from typing import Optional
from pyparsing import Generator

#%%

example = io.StringIO("""#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
""")

def convert(cur_list:list[str]) -> tuple[list[int], list[int]]:
    cols = []
    lines = [0 for _ in cur_list[0]]
    for line in cur_list:
        cur = 0
        for i, c in enumerate(line):
            lines[i] *= 2
            cur *= 2
            if c == "#":
                    lines[i] += 1
                    cur += 1
        cols.append(cur)
    return lines, cols


def read_input(input:io.TextIOBase) -> Generator[tuple[list[int], list[int]], None, None]:
    cur_list = []
    for line in input:
        line = line.rstrip()
        if line:
            cur_list.append(line)
        else:
            yield convert(cur_list)
            cur_list = []
    if cur_list:
        yield convert(cur_list)
            
test_data = list(read_input(example))

def back_convert(i:int):
     return "".join([((c == "1" and "#") or ".") for c in bin(i)[2:]])


# %%

def find_symetrie(line:list[int]) -> int:
    """Search for mirror, mirror are supposed between column"""
    # check from left
    try:
        p = 1
        while True:
            next = line.index(line[0], p)

            if next % 2 == 0:
                p = next + 1
                continue

            found = True
            for i in range((next + 1)//2):
                 if line[i] != line[next - i]:
                      found = False
                      break
            if found:
                 return (next + 1) // 2
            
            p = next + 1

    except ValueError:
         pass
    
    try:
        p = 0
        while True:
            next = line.index(line[-1], p, -1)

            if (len(line) - next) % 2 == 1:
                p = next + 1
                continue

            found = True
            i = 0
            for i in range(1, (len(line) - next)//2):
                 if line[next + i] != line[-i - 1]:
                      found = False
                      break
            if found:
                 return (next + len(line))//2
            
            p = next + 1

    except ValueError:
         pass

    return 0

for l, c in test_data:
     print(find_symetrie(l))
     print(find_symetrie(list(reversed(l))))
     print(find_symetrie(c))
     print(find_symetrie(list(reversed(c))))


# %%


def total(data):
    score = 0
    for line, column in data:
          score += find_symetrie(line) + 100 * find_symetrie(column)
    
    return score

# print(total(test_data))


# %%

    
with open("input-day13.txt") as f:
    data = read_input(f)

    print(total(data))

# %%

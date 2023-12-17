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

p2 = set((2 ** n for n in range(30)))
# %%
test_data
# %%

def check_symetrie(line:list[int], start:int, stop:int) -> bool:
    if line[start] != line[stop] and line[start] ^ line[stop] not in p2:
        return False
    has_change = line[start] ^ line[stop] in p2
    start += 1
    stop -= 1
    while start < stop:
        if line[start] != line[stop]:
            if has_change or line[start] ^ line[stop] not in p2:
                return False
            else:
                has_change = True
        start += 1
        stop -= 1
    return has_change    

#%%

assert check_symetrie(test_data[0][0],1, 8) == False
assert check_symetrie(test_data[0][0],1, 6) == False
assert check_symetrie(test_data[0][1],0, 5) == True
assert check_symetrie(test_data[0][1],1, 6) == False

assert check_symetrie(test_data[1][0],0, 4) == False
assert check_symetrie(test_data[1][0],1, 6) == False
assert check_symetrie(test_data[1][1],0, 1) == True
assert check_symetrie(test_data[1][1],3, 6) == False

#%%


def find_symetrie_bis(line:list[int]) -> int:
    """Search for mirror, mirror are supposed between column"""
    # check from left
    for p in range(1, len(line), 2):
        if check_symetrie(line, 0, p):
            return p//2 + 1

    for p in range(len(line) - 2, 0, -2):
        if check_symetrie(line, p, len(line)-1):
            return p + (len(line) - p)//2
    
    return 0

assert find_symetrie_bis(test_data[0][0]) == 0
assert find_symetrie_bis(test_data[0][1]) == 3
assert find_symetrie_bis(test_data[1][0]) == 0
assert find_symetrie_bis(test_data[1][1]) == 1
assert find_symetrie_bis(list(reversed(test_data[0][1]))) == 4
assert find_symetrie_bis(list(reversed(test_data[1][1]))) == 6
# %%

def total2(data):
    score = 0
    for line, column in data:
          score += find_symetrie_bis(line) + 100 * find_symetrie_bis(column)
    
    return score

print(total2(test_data))

# %%

with open("input-day13.txt") as f:
    data = read_input(f)

    print(total2(data))


# %%

#%%

import io

#%%

example = io.StringIO("""...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
""")

map = set[tuple[int, int]]

def read_data(input:io.TextIOBase) -> map:
    rows = input.readlines()
    star:map = set()
    for i, row in enumerate(rows):
        for j, c in enumerate(row):
            if c == "#":
                star.add((i, j))
    return star

test_data = read_data(example)
print(test_data)
# %%

def missings(data):
    rows:set[int] = {i for i, _ in data}
    columns:set[int] = {j for _, j in data}

    missing_row = {
        a for a in range(min(rows), max(rows)) if a not in rows
    }
    missing_column = {
        b for b in range(min(columns), max(columns)) if b not in columns
    }
    return missing_row, missing_column

test_missing_row, test_missing_column = missings(test_data)

# %%

def dist(p1:tuple[int, int], p2:tuple[int, int], missing_row:set[int], missing_column:set[int], expand = 2):
    expand -= 1
    i1, j1 = p1
    i2, j2 = p2
    d1 = abs(i2-i1) + len(missing_row.intersection(range(min(i1, i2), max(i1, i2)))) * expand
    d2 = abs(j2-j1) + len(missing_column.intersection(range(min(j1, j2), max(j1, j2)))) * expand
    return d1 + d2

test_pt = [(0, 3), (1, 7), (2, 0), (4, 6), (5, 1), (6, 9), (8, 7), (9, 0), (9, 4)]

assert dist(test_pt[4], test_pt[8], test_missing_row, test_missing_column) == 9
assert dist(test_pt[8], test_pt[4], test_missing_row, test_missing_column) == 9
assert dist(test_pt[0], test_pt[6], test_missing_row, test_missing_column) == 15
assert dist(test_pt[6], test_pt[0], test_missing_row, test_missing_column) == 15
assert dist(test_pt[5], test_pt[2], test_missing_row, test_missing_column) == 17
assert dist(test_pt[2], test_pt[5], test_missing_row, test_missing_column) == 17
assert dist(test_pt[8], test_pt[7], test_missing_row, test_missing_column) == 5
assert dist(test_pt[7], test_pt[8], test_missing_row, test_missing_column) == 5
# %%
def total(data, expand = 2):
    missing_row, missing_column = missings(data)
    tot = 0
    nb = 0
    li = list(data)
    for i, pt1 in enumerate(li):
        for j in range(i+1, len(li)):
            pt2 = li[j]
            tot += dist(pt1, pt2, missing_row, missing_column, expand)
            nb += 1
    return tot



print(total(test_data))

assert total(test_data) == 374



# %%

with open("input-day11.txt") as f:
    data = read_data(f)

print(total(data))
# %%
assert total(test_data, 10) == 1030
assert total(test_data, 100) == 8410

# %%
print(total(data, 1000000))

# %%

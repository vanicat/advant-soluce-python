#%%

from collections import deque
from collections.abc import Generator, Sequence


#%%


example_st = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""

with open("input-day23.txt") as f:
    problem_st = f.read()

example:list[str] = example_st.split() # type: ignore
problem = problem_st.split()

# %%

dep = (
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1)
)

def explore(labyrinthe:list[str]) -> Generator[int, None, None]:
    i = 0
    j = None
    for j, c in enumerate(labyrinthe[0]):
        if c == ".":
            break
    assert j is not None
    seen = set()
    yield from explore_rec(i, j, labyrinthe, seen, 0)


def explore_rec(i:int, j:int, labyrinthe:list[str], seen:set[tuple[int, int]], step:int) -> Generator[int, None, None]:
    pos = (i, j)
    if pos in seen:
        return
    if i == len(labyrinthe) - 1:
        yield step 
        return
    seen.add(pos)
    for di, dj in dep:
        ni = i + di
        nj = j + dj
        match labyrinthe[ni][nj]:
            case ".":
                yield from explore_rec(ni, nj, labyrinthe, seen, step + 1)
            case "^":
                yield from explore_rec(ni-1, nj, labyrinthe, seen, step + 2)
            case ">":
                yield from explore_rec(ni, nj+1, labyrinthe, seen, step + 2)
            case "v":
                yield from explore_rec(ni+1, nj, labyrinthe, seen, step + 2)
            case "<":
                yield from explore_rec(ni, nj-1, labyrinthe, seen, step + 2)
    seen.remove(pos)


print("example")
for i in explore(example):
    print(i)

print("problem")
for i in explore(problem):
    print(i)
print(max(explore(problem)))


# %%
def explore2(labyrinthe:list[str]) -> Generator[int, None, None]:
    i = 0
    j = None
    for j, c in enumerate(labyrinthe[0]):
        if c == ".":
            break
    assert j is not None
    seen = set()

    stack = deque()
    stack.append((i, j, 0))
    seen.add((i, j))
    while stack:
        i, j, n = stack.pop()
        if n >= 4:
            seen.remove((i, j))
            continue
        stack.append((i, j, n + 1))
        di, dj = dep[n]
        ni = i + di
        nj = j + dj
        if labyrinthe[ni][nj] == "#":
            continue
        if (ni, nj) in seen:
            continue
        if ni == len(labyrinthe) - 1:
            yield len(seen)
            continue
        seen.add((ni, nj))
        stack.append((ni, nj, 0))


print("example")
for i in explore2(example):
    print(i)

print("problem")
m = 0
c = 0
for i in explore2(problem):
    if i > m:
        m = i
    c = c + 1
    if c & 0b111111111111 == 0:
        print(i, m) 
print(max(explore(problem)))

# %%

#%%
from enum import Enum, auto
import heapq
import io
from math import inf
from typing import Generator, Optional, Self
#%%

example = io.StringIO("""2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
""")
example2 = io.StringIO("""111111111111
999999999991
999999999991
999999999991
999999999991
""")


class Direction(Enum):
    UPWARD=auto()
    DOWNWARD=auto()
    RIGHTWARD=auto()
    LEFTWARD=auto()

    def __ge__(self, other):
        if isinstance(other, Direction):
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Direction):
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Direction):
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Direction):
            return self.value < other.value
        return NotImplemented


def turn(dir:Direction):
    match dir:
        case Direction.UPWARD | Direction.DOWNWARD:
            yield Direction.RIGHTWARD
            yield Direction.LEFTWARD
        case _:
            yield Direction.UPWARD
            yield Direction.DOWNWARD


def move(i:int, j:int, dir:Direction) -> tuple[int, int]:
    match dir:
        case Direction.UPWARD:
            return (i - 1, j)
        case Direction.LEFTWARD:
            return (i, j - 1)
        case Direction.RIGHTWARD:
            return (i, j + 1)
        case Direction.DOWNWARD:
            return (i + 1, j)


def dist(i1:int, j1:int, i2:int, j2:int) -> int:
    return abs(i1-i2) + abs(j1 - j2)


class Location:
    value:int
    step_dist:list[list[int]]
    step_done:list[list[bool]]
    step_from:list[list[Optional[tuple[int, int, Direction, int]]]]


    def __init__(self, value:int, i:int, j:int) -> None:
        self.value = value
        self.i = i
        self.j = j
        self.reinit()


    def reinit(self, n=3, min=0):
        self.step_dist = [[inf] * n for _ in range(4)] # type: ignore
        self.step_done = [[False] * n for _ in range(4)]
        self.step_from = [[None] * n for _ in range(4)]
        self.n = n
        self.min = min

    
    def next(self, dir:Direction, k) -> Generator[tuple[int, int, Direction, int], None, None]:
        if k < self.n - 1:
            yield (*move(self.i, self.j, dir), dir, k+1)
        if k >= self.min - 1:
            for next_dir in turn(dir):
                yield (*move(self.i, self.j, next_dir), next_dir, 0)


    def set(self, dir:Direction, k:int, dist:int, from_:Optional[tuple[int, int]]) -> Generator[int, None, None]: 
        for i in range(k, min(k+1, self.n)):
            if dist < self.step_dist[dir.value - 1][i]:
                self.step_dist[dir.value - 1][i] = dist
                if from_:
                    self.step_from[dir.value - 1][i] = (*from_, dir, i)
                else:
                    self.step_from[dir.value - 1][i] = None
                yield i

    def mark(self, dir:Direction, k:int, dist:int) -> None: 
        for i in range(k, self.n):
            if self.step_dist[dir.value - 1][i] <= dist:
                self.step_done[dir.value - 1][i] = True


    def marked(self, dir:Direction, k:int) -> bool: 
        return self.step_done[dir.value - 1][k]
    
    def __repr__(self):
        for line in self.step_done:
            for k in line:
                if k:
                    return "*"
        for line in self.step_dist:
            for k in line:
                if k < inf:
                    return "."
        return str(self.value)
        

Map = list[list[Location]]

def read_input(input:io.TextIOBase) -> Map:
    map:"Map" = []
    for i, line in enumerate(input):
        line = line.strip()
        new_line:list[Location] = []
        for j, c in enumerate(line):
            new_line.append(Location(int(c), i, j))
        map.append(new_line)
    return map

test_data = read_input(example)
test_data2 = read_input(example2)

def disp(map:Map):
    for line in map:
        for loc in line:
            print(f"{min((min(l) for l in loc.step_dist)):4}", end="")
        print()


# %%

def astar(map:Map, n=3, min=0):
    for line in map:
        for loc in line:
            loc.reinit(n=n, min=min)
    dist = map[0][0].value * 0
    list(map[0][0].set(Direction.RIGHTWARD, 0, dist, None))
    height = len(map)
    width = len(map[0])
    queue:list[tuple[int, int, int, int, Direction]] = [(dist, 0, 0, 0, Direction.RIGHTWARD)]
    while queue:
        dist, k, i, j, dir = heapq.heappop(queue)
        if i == height - 1 and j == width - 1 and k >= min:
            return dist
        loc:Location = map[i][j]
        if loc.marked(dir, k):
            continue
        loc.mark(dir, k, dist)
        for ni, nj, ndir, nk in loc.next(dir, k):
            if 0 <= ni < height and 0 <= nj < width:
                nloc = map[ni][nj]
                ndist = dist + map[ni][nj].value
                for add_k in nloc.set(ndir, nk, ndist, (i, j)):
                    heapq.heappush(queue, (ndist, add_k, ni, nj, ndir))

def trajet(map:Map):
    loc = map[-1][-1]
    d = None
    for i in reversed(range(len(loc.step_from))):
        if loc.step_from[i] != [None, None, None]:
            d = i

    assert d is not None
    dir = Direction(d)
    k = None
    for i in reversed(range(len(loc.step_from[d]))):
        if loc.step_from[d][i] is not None:
            k = i

    assert k is not None
    return dir, k
    


    return d


print(astar(test_data))
print(trajet(test_data))
print(trajet(test_data))
# %%
with open("input-day17.txt") as f:
    data = read_input(f)
    #print(astar(data))



# %%
print(astar(test_data, n=10, min=4))
print(astar(test_data2, n=10, min=4))

print(astar(data, n=10, min=4))


# %%
def show_loc_traj(data, i, j):
    print(i, j)
    for d in range(4):
        dir = Direction(d + 1)
        print(dir, data[i][j].step_from[d], data[i][j].step_dist[d], "to:", move(i, j, dir))

show_loc_traj(data, -1, -1)

# %%

disp(data)
# %%

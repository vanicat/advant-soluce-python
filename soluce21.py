#%%

import io
from collections.abc import Container, Iterable, Mapping, Sequence

#%%

dep = [
    (-1, 0), 
    (1, 0),
    (0, 1),
    (0, -1)
]

coord = tuple[int, int]

class Explorer:
    avance: set[tuple[coord, coord]]
    clignote: list[list[set[coord]]]
    height: int
    width: int

    def __init__(self, start: coord, height:int, width:int) -> None:
        self.avance = set()
        self.avance.add((start, (0, 0)))
        self.clignote = [[set() for _ in range(width)] for _ in range(height)]
        self.height = height
        self.width = width


    def mvt(self) -> None:
        new_avance = set()
        for ((i, j), (dep_i, dep_j)) in self.avance:
            for di, dj in dep:
                ni = (i + di) % self.height
                nj = (j + dj) % self.width
                xi = (i + di) // self.height
                xj = (j + dj) // self.width
                




class Map:
    wall: set[coord]
    start: coord
    width: int
    height: int

    def __init__(self, map:Sequence[str]) -> None:
        self.wall = set()
        self.height = len(map)
        self.width = len(map[0])

        for i, line in enumerate(map):
            for j, c in enumerate(line):
                match c:
                    case "#":
                        self.wall.add((i, j))
                    case "S":
                        self.start = (i, j)
        
    def step(self, pos:Iterable[coord]) -> set[coord]:
        result = set()
        for i, j in pos:
            for di, dj in dep:
                ni = i + di
                nj = j + dj
                if ni >= 0 and nj >= 0 and ni < self.height and nj < self.width:
                    if (ni, nj) not in self.wall:
                        result.add((ni, nj))

        return result
    
    def walk(self, n:int) -> set[coord]:
        l:set[coord] = set((self.start,))
        for _ in range(n):
            l = self.step(l)
        
        return l
        
    def step_long(self, pos:Mapping[coord, set[coord]]) -> dict[coord, set[coord]]:
        result:dict[coord, set[coord]] = dict()
        for i, j in pos:
            for di, dj in dep:
                ni = (i + di) % self.height
                nj = (j + dj) % self.width
                if (ni, nj) not in self.wall:
                    if (ni, nj) not in result:
                        result[(ni, nj)] = set()
                    result[(ni, nj)].add((0, 0))


        return result
    
    def walk_long(self, n:int) -> set[coord]:
        l:set[coord] = set((self.start,))
        for _ in range(n):
            l = self.step(l)
        
        return l
    
    def __str__(self) -> str:
        return "\n".join([
            "".join([
               "#" if (i, j) in self.wall else "." for j in range(self.width)
            ]) for i in range(self.height)
        ])

    def disp_pos(self, pos:Container[coord]):
        def loc(i, j) -> str:
            if (i, j) in self.wall:
                return "#"
            elif (i, j) in pos:
                return "O"
            elif (i, j) == self.start:
                return "S"
            else:
                return "."
        return "\n".join([
            "".join([
               loc(i, j) for j in range(self.width)
            ]) for i in range(self.height)
        ])

#%%h

example = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
""".split()

example_map = Map(example)
print(example_map)

example_pos = example_map.walk(6)
print(example_map.disp_pos(example_pos))
print(len(example_pos))

# %%

with open("input-day21.txt") as f:
    problem = Map([line.strip() for line in f])

print(problem)

#%%

final = problem.walk(64)
print(len(final))
# %%

start:dict[coord, set[coord]] = { problem.start: set(((0, 0), )) }
pos = start

# %%
pos = problem.step_long(pos)
print(problem.disp_pos(pos))
# %%

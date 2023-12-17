#%%

from dataclasses import dataclass
import io
import timeit
from typing import Optional
from pyparsing import Generator

#%%

example = io.StringIO("""O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
""")

class Map:
    map: set[tuple[int, int]]
    rocks: list[list[bool]]
    width: int
    height: int

    def __init__(self, width:int, height:int) -> None:
        self.width = width
        self.height = height
        self.map = set()
        self.rocks = [[False for _ in range(width)] for _ in range(height)]

    def add_elem(self, r:int, c:int, elem:str) -> None:
        match elem:
            case "O":
                self.rocks[r][c] = True
            case "#":
                self.map.add((r, c))


    def __getitem__(self, pos:tuple[int, int]) -> bool:
        return pos in self.map or self.rocks[pos[0]][pos[1]]
    
    def move_north(self):
        for c in range(self.width):
            for r in range(self.height):
                if self.rocks[r][c]:
                    dest = r - 1
                    while dest >= 0 and not self[(dest, c)]:
                        dest -= 1
                    dest += 1
                    self.rocks[r][c] = False
                    self.rocks[dest][c] = True

    def move_south(self):
        for c in range(self.width):
            for r in reversed(range(self.height)):
                if self.rocks[r][c]:
                    dest = r + 1
                    while dest < self.height and not self[(dest, c)]:
                        dest += 1
                    dest -= 1
                    self.rocks[r][c] = False
                    self.rocks[dest][c] = True

    def move_west(self):
        for c in range(self.width):
            for r in range(self.height):
                if self.rocks[r][c]:
                    dest = c - 1
                    while dest >= 0 and not self[(r, dest)]:
                        dest -= 1
                    dest += 1
                    self.rocks[r][c] = False
                    self.rocks[r][dest] = True

    def move_east(self):
        for c in reversed(range(self.width)):
            for r in range(self.height):
                if self.rocks[r][c]:
                    dest = c + 1
                    while dest < self.height and not self[(r, dest)]:
                        dest += 1
                    dest -= 1
                    self.rocks[r][c] = False
                    self.rocks[r][dest] = True

    def cycle(self):
        self.move_north()
        self.move_west()
        self.move_south()
        self.move_east()


    def load(self) -> int:
        score = 0
        for l, line in enumerate(reversed(self.rocks)):
            score += (l + 1) * sum(line)

        return score

    def lines(self) -> Generator[str, None, None]:
        for r in range(self.height):
            line = []
            for c in range(self.width):
                if (r, c) in self.map:
                    line.append("#")
                elif self.rocks[r][c]:
                    line.append("O")
                else:
                    line.append(".")
            yield "".join(line)

    def __str__(self) -> str:
        return "\n".join(self.lines())

    




def read_input(input:io.TextIOBase) -> Map:
    li = input.readlines()
    height = len(li)
    width = len(li[0]) - 1
    m = Map(width, height)
    for r, line in enumerate(li):
        for c, elem in enumerate(line):
            m.add_elem(r, c, elem)
    return m


def make_test_data(): 
    example = io.StringIO("""O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
""")
    return read_input(example)

test_data = read_input(example)
def compute(data:Map):
    data.move_north()
    return(data.load())

# print(compute(test_data))
# %%


    
with open("input-day14.txt") as f:
    data = read_input(f)

    print(compute(data))
# %%

for _ in range(3):
    test_data.cycle()
    print(test_data)
    print()


# %%
test_data = make_test_data()

print(timeit.timeit("test_data.cycle()", globals=globals(), number=10000))

situation = str(test_data)
for i in range(6000):
    test_data.cycle()


print(test_data.load())
# %%

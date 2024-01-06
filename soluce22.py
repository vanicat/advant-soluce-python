#%%

from collections.abc import Container, Generator, Iterable, Mapping, Sequence
from dataclasses import dataclass
import functools
from heapq import heapify, heappop, heappush
from typing import Literal, Self, assert_type, cast

#%%

example = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""

with open("input-day22.txt") as f:
    problem_st = f.read()

#%% 

last_name = 0

@dataclass
@functools.total_ordering
class Bloc:
    name: int
    minx: int
    miny: int
    minz: int
    maxx: int
    maxy: int
    maxz: int

    support: set[Self]
    supporting: set[Self]
    disintegrable: bool = True

    def move(self, new_minz:int) -> None:
        self.maxz += new_minz - self.minz
        self.minz = new_minz

    def __lt__(self, other):
        if isinstance(other, Bloc):
            if self.minz != other.minz:
                return self.minz < other.minz
            elif self.maxz != other.maxz:
                return self.maxz < other.maxz
            elif self.name != other.name:
                return self.name < other.name
            elif self.minx != other.minx:
                return self.minx < other.minx
            else:
                return self.miny < other.miny
        return NotImplemented
    
    def __hash__(self) -> int:
        return hash((self.name, self.minx, self.miny, self.minz, self.maxx, self.maxy, self.maxz))

    @classmethod
    def read(cls, line) -> Self:
        global last_name
        line = line.strip()
        deb, fin = line.split("~")
        x1, y1, z1 = (int(s) for s in deb.split(","))
        x2, y2, z2 = (int(s) for s in fin.split(","))
        last_name += 1

        return cls(last_name,
                   min(x1, x2), min(y1, y2), min(z1, z2),
                   max(x1, x2), max(y1, y2), max(z1, z2), 
                   set(), set())
    
    @classmethod
    def read_pb(cls, lines) -> list[Self]:
        global last_name
        last_name = 0
        return [cls.read(line) for line in lines.split("\n") if line]
    
    def coords(self) -> Generator[tuple[int, int], None, None]:
        for i in range(self.minx, self.maxx + 1):
            for j in range(self.miny, self.maxy + 1):
                yield (i, j)

example_pb = Bloc.read_pb(example)
problem = Bloc.read_pb(problem_st)
# %%

def descente(pb:list[Bloc]) -> None:
    pb.sort()
    # minx = min((bl.minx for bl in pb))
    # miny = min((bl.miny for bl in pb))
    maxx = max((bl.maxx for bl in pb))
    maxy = max((bl.miny for bl in pb))
    
    bufz:list[list[tuple[Literal[0], None] | tuple[int, Bloc]]] = [
        [ (0, None) for _ in range(maxy + 1)]
        for _ in range(maxx + 1)
    ]

    for bl in pb:
        support:set[Bloc] = set()
        support_z = 0
        for x, y in bl.coords():
            z, below = bufz[x][y]
            if z == 0 or z < support_z:
                continue
            below = cast(Bloc, below)
            if z == support_z:
                if z != 0:
                    support.add(below)
            else:
                support = set((below,))
                support_z = z

        bl.support = support
        for s in support:
            s.supporting.add(bl)

        print(f"moving {bl.name} from {bl.minz} to {support_z + 1} on {[b.name for b in bl.support]}")    
        bl.move(support_z + 1)
        for x, y in bl.coords():
            bufz[x][y] = (bl.maxz, bl)

# %%
            
print("example")
descente(example_pb)
print("\n \nproblem")
descente(problem)

# %%

def score1(problem:list[Bloc]):
    disintregrable = set(problem)
    for bl in problem:
        if len(bl.support) == 1:
            support = next(iter(bl.support))
            if support in disintregrable:
                disintregrable.remove(support)    
    return len(disintregrable)

print(score1(example_pb))
print(score1(problem))
# %%

def score2(problem:list[Bloc]) -> int:
    total = 0
    for bl in problem:
        falling = set()
        falling.add(bl)
        may_fall = list(bl.supporting)
        heapify(may_fall)
        while may_fall:
            elem = heappop(may_fall)        
            if elem.support.issubset(falling):
                falling.add(elem)
                for up in elem.supporting:
                    heappush(may_fall, up)
        total += len(falling) - 1

    return total

print(score2(example_pb))
print(score2(problem))


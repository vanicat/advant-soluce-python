#%%

from collections.abc import Generator, Iterable
from dataclasses import dataclass
from enum import Enum, auto
from heapq import heappop, heappush
import math
from typing import Optional, Self, cast

#%%

example_st = cast(str, """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
""")

@dataclass
class Hailstone:
    px:int
    py:int
    pz:int

    vx:int
    vy:int
    vz:int

    @classmethod
    def read(cls, st:str) -> Self:
        p, v = st.split(" @ ")
        px, py, pz = [int(x.strip()) for x in p.split(",")]
        vx, vy, vz = [int(x.strip()) for x in v.split(",")]
        return cls(px, py, pz, vx, vy, vz)

assert Hailstone.read("19, 13, 30 @ -2,  1, -2\n") == Hailstone(19, 13, 30, -2, 1, -2)

@dataclass
class Problem:
    stones: list[Hailstone]
    min: int
    max: int

    @classmethod
    def read(cls, st:str, min:int, max:int) -> Self:
        lines = st.split("\n")
        stones = [Hailstone.read(l) for l in lines if l]
        return cls(stones, min, max)
    
    @property
    def segments(self) -> "Generator[Segment, None, None]":
        for st in self.stones:
            seg = Segment.generate(st, self.min, self.max)
            if seg is not None:
                yield seg

    

    
example = Problem.read(example_st, 7, 27)
assert len(example.stones) == 5


# %%

with open("input-day24.txt") as f:
    problem_st = f.read()

problem = Problem.read(problem_st, 200000000000000, 400000000000000)

# %%

@dataclass(frozen=True)
class Segment:
    x1: float
    y1: float
    x2: float
    y2: float
    a: float

    @classmethod
    def generate(cls, h:Hailstone, at_least:int, at_most:int) -> Optional[Self]:
        def calc_λ(x:float, m:float, v:float, y:float, vy:float) -> tuple[float, float, float]:
            λ = (m - x) / v
            ny = y + λ * vy
            return λ, m, ny
        
        x = h.px
        y = h.py
        def pts():
            yield (0, x, y)
            yield calc_λ(x, at_least, h.vx, y, h.vy)
            yield calc_λ(x, at_most, h.vx, y, h.vy)
            λ3, y3, x3 = calc_λ(y, at_least, h.vy, x, h.vx)
            yield λ3, x3, y3
            λ4, y4, x4 = calc_λ(y, at_most, h.vy, x, h.vx)
            yield λ4, x4, y4

        def verif(λ, x, y):
            return λ >= 0 and at_least <= x <= at_most and at_least <= y <= at_most 

        li = [(x, y) for λ, x, y in pts() if verif(λ, x, y)]

        if li == []:
            return

        x0, y0 = min(li)
        x1, y1 = max(li)
        assert x0 < x1
        return cls(x0, y0, x1, y1, h.vy/h.vx)
    
    def intersection(self, other:Self) -> Optional[tuple[float, float]]:
        if self.a == other.a:
            return
        dox = ((other.y1 - self.y1) - self.a * (other.x1 - self.x1)) / (self.a - other.a)
        x = other.x1 + dox
        if not (self.x1 <= x <= self.x2 and other.x1 <= x <= other.x2):
            return
        y = other.y1 + other.a * dox
        return (x, y)
    
    def __contains__(self, pt:tuple[float, float]):
        if isinstance(pt, tuple) and len(pt) == 2:
            x, y = pt
            return self.a * (x - self.x1) == (x - self.y1)
        
    def ordinate(self, x:float):
        if x == self.x2:
            return self.y2
        return self.y1 + self.a * (x - self.x1) 
        
    
#%%
for st in example.stones:
    print(st, Segment.generate(st, example.min, example.max))

#%%
for seg in problem.segments:
    print(seg)

# %%

s1 = Segment(1, 1, 10, 10, 1)
s2 = Segment(1, 3, 10, 3, 0)
assert s1.intersection(s2) is not None
assert s1.intersection(s2) == s2.intersection(s1)
assert s1.intersection(s2) in s1 # type: ignore
assert s1.intersection(s2) in s2 # type: ignore
assert s1.intersection(s2)[1] == 3 # type: ignore
s3 = Segment(1, 3, 11, 23, 2)
assert s1.intersection(s3) is None

s4 = Segment(0, 1, 3, 3, 2/3)
s5 = Segment(0, 3, 3, 1, -2/3)
assert s4.intersection(s5) is not None
assert s4.intersection(s5)[0] == 1.5 # type: ignore
assert s4.intersection(s5)[1] == 2 # type: ignore

# %%

class EventType(Enum):
    start = auto()
    intersect = auto()
    end = auto()

@dataclass
class Event:
    type: EventType
    x: float
    y: float
    s1: Segment
    s2: Optional[Segment] = None

    def __lt__(self, other) -> bool:
        if isinstance(other, Event):
            if self is other:
                return False
            if self.x != other.x: 
                return self.x < other.x
            if self.y != other.y:
                return self.y < other.y
            if self.type != other.type:
                if self.type == EventType.start:
                    return True
                if other.type == EventType.start:
                    return False
                return self.type == EventType.intersect

        return NotImplemented


def insert_pos(ord:list[Segment], x:float, y:float):
    start = 0
    stop = len(ord)
    while start < stop:
        mid = (start + stop) // 2
        y_mid = ord[mid].ordinate(x) 
        if math.isclose(y, y_mid):
            return mid
        elif y < y_mid:
            stop = mid
        else:
            start = mid + 1
    
    assert start == stop

    return start


def intersect(segments: Iterable[Segment]):
    plist:list[Event] = []
    for s in segments:
        heappush(plist, (Event(EventType.start, s.x1, s.y1, s)))
        heappush(plist, (Event(EventType.end, s.x2, s.y2, s)))
    
    ordered = []
    intersected = set()

    while plist:
        ev = heappop(plist)
        match ev.type:
            case EventType.start:
                i = insert_pos(ordered, ev.x, ev.y)
                if i-1 >= 0:
                    may_add_intersect(plist, intersected, ev.s1, ordered[i-1])
                if i < len(ordered):
                    may_add_intersect(plist, intersected, ev.s1, ordered[i])
                ordered.insert(i, ev.s1)
            case EventType.intersect:
                i = insert_pos(ordered, ev.x, ev.y)
                assert 0 <= i < len(ordered)
                s1 = ev.s1
                s2 = cast(Segment, ev.s2)
                j = None
                if i - 1 >= 0:
                    if ordered[i-1] is s1 and ordered[i] is s2:
                        i, j = i - 1, i
                    elif ordered[i] is s1 and ordered[i-1] is s2:
                        s1, s2 = s2, s1
                        i, j = i - 1, i
                if i + 1 < len(ordered):
                    if ordered[i] is s1 and ordered[i+1] is s2:
                        i, j = i, i + 1
                    elif ordered[i + 1] is s1 and ordered[i] is s2:
                        s1, s2 = s2, s1
                        i, j = i, i + 1
                assert j is not None
                ordered[i] = s2
                ordered[j] = s1
                if i - 1 >= 0:
                    may_add_intersect(plist, intersected, s2, ordered[i-1])
                if j + 1 < len(ordered):
                    may_add_intersect(plist, intersected, s1, ordered[j+1])
            case EventType.end:
                i = insert_pos(ordered, ev.x, ev.y)
                assert ordered[i] is ev.s1
                del ordered[i]
                if i - 1 >= 0 and i < len(ordered):
                    may_add_intersect(plist, intersected, ordered[i-1], ordered[i])
    return intersected
                

def may_add_intersect(plist:list[Event], intersected:set, s1:Segment, s2:Segment):
    it = s1.intersection(s2)
    if it:
        x, y = it
        both = frozenset((s1, s2))
        if both not in intersected:
            intersected.add(both)
            heappush(plist, Event(EventType.intersect, x, y, s1, s2))

intersect(example.segments)
# %%
print(len(intersect(problem.segments)))
# %%

import sympy as sp

def make_eqn(pb:Problem):
    x, y, z, vx, vy, vz = sp.symbols("x y z vx vy vz")

    for i, h in enumerate(pb.stones):
        ti = sp.Symbol(f"t{i}")
        yield x + ti * vx - h.px - h.vx * ti
        yield y + ti * vy - h.py - ti * h.vy
        yield z + ti * vz - h.pz - ti * h.vz
        


print(list(make_eqn(example)))
print(sp.solve(make_eqn(example)))
print(sp.solve(make_eqn(problem)))
# %%
print(363206674204110 + 368909610239045 + 156592420220258)
# %%

#%%
from dataclasses import dataclass
import functools
import io
import re
from typing import Generator, Iterable, Optional, Self

#%%

example_str = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

example2_str = """R 6 (#000030)
R 6 (#000013)
R 6 (#000040)
R 6 (#000041)
R 6 (#000030)
R 6 (#000031)
R 6 (#000032)
R 6 (#000023)
R 6 (#000022)
R 6 (#000033)
R 6 (#000032)
R 6 (#000021)
R 6 (#000022)
R 6 (#000033)
"""

Instruction = tuple[str, int, str]

def read_input(input:io.TextIOBase) -> "Generator[Instruction, None, None]":
    for line in input:
        me = re.match(r"(.) ([0-9]+) \((.*)\)\n", line)
        assert me is not None, f"incorrect line: {line}"
        yield me.group(1), int(me.group(2)), me.group(3)

def read_exemple(str:str) -> "Generator[Instruction, None, None]":
    example = io.StringIO(str)
    yield from read_input(example)

debug_data = list(read_exemple(example_str))
# %%
def move(instruction:Iterable[Instruction]):
    i = 0
    j = 0
    for d, mvt, color in instruction:
        match d:
            case "R":
                for j in range(j + 1, j + mvt + 1):
                    yield (i, j)
            case "D":
                for i in range(i + 1, i + mvt + 1):
                    yield (i, j)
            case "L":
                for j in range(j - 1, j - mvt - 1, -1):
                    yield (i, j)
            case "U":
                for i in range(i - 1, i - mvt - 1, -1):
                    yield (i, j)

# %%

def dig(instruction:Iterable[Instruction]):
    hole = set(move(instruction))
    mini = min((i for i, _ in hole))
    minj = min((j for _, j in hole))

    depi = None
    depj = None

    for i, j in hole:
        if i == mini and (i, j-1) in hole and (i, j+1) in hole:
            depi = i + 1
            depj = j
            break
        if j == minj and (i-1, j) in hole and (i+1, j) in hole:
            depi = i
            depj = j + 1

    assert depi is not None and depj is not None, f"no start point"

    look_at = [(depi, depj)]
    hole.add((depi, depj))
    
    while look_at:
        i, j = look_at.pop()
        for next in ((i+1, j), (i-1, j), (i, j-1), (i, j+1)):
            if next not in hole:
                look_at.append(next)
                hole.add(next)

    return hole


len(dig(read_exemple(example_str)))

# %%
with open("input-18") as f:
    print(len(dig(read_input(f))))
# %%

direction_array = ["R", "D", "L", "U"]

def read_exa(st) -> tuple[str, int]:
    return direction_array[int(st[6])], int(st[1:6], 16)

@dataclass(order=True)
class H_Line:
    i: int
    depj:int
    endj:int

    def surface(self, i:int, addone = False) -> int:
        return (i - self.i + int(addone)) * (self.endj - self.depj + 1)

    def concat(self, other:Self) -> "H_Line":
        i = max(self.i, other.i)
        if self.endj == other.depj:
            return H_Line(i, self.depj, other.endj)
        if self.depj == other.endj:
            return H_Line(i, other.depj, self.endj)
        if self.depj == other.depj:
            return H_Line(i, min(self.endj, other.endj), (max(self.endj, other.endj)))
        if self.endj == other.endj:
            return H_Line(i, min(self.depj, other.depj), (max(self.depj, other.depj)))

        raise ValueError(self, other)
    
    def remove(self, other:Self) -> "tuple[H_Line, H_Line]":
        i = max(self.i, other.i)
        return (
            H_Line(i, self.depj, other.depj ),
            H_Line(i, other.endj, self.endj)
        )


def move_long(instruction:Iterable[Instruction], i = 0) -> Generator[H_Line, None, None]:
    j = 0
    for _, _, color in instruction:
        d, length = read_exa(color)
        match d:
            case "R":
                yield H_Line(i, j, j + length)
                j = j + length
            case "D":
                i = i + length
            case "L":
                yield H_Line(i, j - length, j)
                j = j - length
            case "U":
                i = i - length
 

li_exemple = list(move_long(read_exemple(example_str)))
li_exemple.sort()
print(li_exemple)

#%%

class Rectangles:
    def __init__(self) -> None:
        self.rectangles:dict[int, H_Line] = {}

    def add_rectangle(self, h:H_Line) -> None:
        self.rectangles[h.depj] = h
        self.rectangles[h.endj] = h

    def get_rectangle(self, j:int) -> Optional[H_Line]:
        if j in self.rectangles:
            h = self.rectangles[j]
            del self.rectangles[j]
            return h
        
    def get_include_rectangle(self, j) -> Optional[H_Line]:
        for rect in self.rectangles.values():
            if rect.depj < j < rect.endj:
                del self.rectangles[rect.depj]
                del self.rectangles[rect.endj]
                return rect
            


#%%
def surface(instruction:Iterable[Instruction]):
    evts = list(move_long(instruction, 2))
    evts.sort()

    total = 0
    rects = Rectangles()

    for ev in evts:
        left = rects.get_rectangle(ev.depj)
        right = rects.get_rectangle(ev.endj)
        if left is not None and right is not None:
            if left is right:
                total += left.surface(ev.i)
            else:
                total += left.surface(ev.i)
                total += right.surface(ev.i)
                bare = ev.concat(left).concat(right)
                total += bare.surface(ev.i, True)

                rects.add_rectangle(bare)

        elif left is not None:
            bare = ev.concat(left)
            rects.add_rectangle(bare)

            if left.endj == ev.depj:
                total += left.surface(ev.i - 1)
                total += bare.surface(ev.i, True)
            else:
                total += left.surface(ev.i)

        elif right is not None:
            bare = ev.concat(right)
            rects.add_rectangle(bare)

            if right.depj == ev.endj:
                total += right.surface(ev.i - 1)
                total += bare.surface(ev.i, True)
            else:
                total += right.surface(ev.i)

        else:
            contain = rects.get_include_rectangle(ev.depj)
            if contain is None:
                rects.add_rectangle(ev)
                total += ev.surface(ev.i, True)
            else:
                total += contain.surface(ev.i)
                deb, fin = contain.remove(ev)
                rects.add_rectangle(deb)
                rects.add_rectangle(fin)

    return total

plan_ex2 = """
   #####
########
########
###  ###
###  ######
     ######
       ####
       ####
"""
print(surface(read_exemple(example_str)))
print(surface(read_exemple(example2_str)), len([x for x in plan_ex2 if x == "#"]))

with open("input-18") as f:
    print(surface(read_input(f)))

# %%

with open("input-18") as f:
    hlines = (list(move_long(read_input(f))))
# %%
print("i", min((t.i for t in hlines)), max((t.i for t in hlines)))
print("j", min((t.depj for t in hlines)), max((t.endj for t in hlines)))
# %%
# %%

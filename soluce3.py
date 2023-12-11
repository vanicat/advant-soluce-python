#%%

from typing import Self

#%%

with open("input-day3.txt") as input:
    text = [st.strip() for st in input.readlines()]

test_text = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""".split()


class Symbol:
    symb: str
    x: int
    y: int

    def __init__(self, line:str, x:int, y:int) -> None:
        self.symb = line[x]
        self.x = x
        self.y = y

    def mark_adjacent(self, map:"Schematic") -> None:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                pos = (self.x + dx, self.y + dy)
                map[pos].mark()

    def mark(self) -> None:
        pass

    def __repr__(self) -> str:
        return f"Symbol({self.symb}, {self.x}, {self.y})"
    
    def gear_ratio(self, map:"Schematic") -> int:
        adjacent_num: set[Num] = set()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                pos = (self.x + dx, self.y + dy)
                elem = map[pos]
                if isinstance(elem, Num):
                    adjacent_num.add(elem)
        if len(adjacent_num) == 2:
            n1, n2 = iter(adjacent_num)
            return n1.value * n2.value
        else:
            return 0
        
class Num:
    value: int
    pos:dict[tuple[int, int], Self] = {}
    marked:bool = False
    initialized = False
    
    def __new__(cls, line:str, x:int, y:int) -> Self:
        if x > 0 and line[x-1].isdigit():
            last: Self = cls.pos[(x-1, y)]
            cls.pos[(x, y)] = last
            return last

        obj: Self = object.__new__(cls)
        cls.pos[(x, y)] = obj
        return obj

    
    def __init__(self, line:str, x:int, y:int) -> None:
        if self.initialized:
            return
        
        end: int = x
        while end < len(line) and line[end].isdigit():
            end = end + 1
        self.value = int(line[x:end])
        self.initialized = True

    def mark_adjacent(self, map:"Schematic") -> None:
        pass

    def mark(self) -> None:
        self.marked = True
    
    def __repr__(self) -> str:
        return f"Num({self.value}, marked={self.marked})"

class Empty:
    def mark_adjacent(self, map:"Schematic") -> None:
        pass

    def mark(self) -> None:
        pass

    def __repr__(self) -> str:
        return "Empty()"

class Schematic:
    pos: dict[tuple[int, int], Empty | Num | Symbol]
    _nums: set[Num]

    def __init__(self, schematic):
        self.pos = {}
        self._nums = set()
        Num.pos = {}
        empt = Empty()
        for y, line in enumerate(schematic):
            for x, car in enumerate(line):
                if car == ".":
                    elem = empt
                elif car.isdigit():
                    elem = Num(line, x, y)
                    self._nums.add(elem)
                else:
                    elem = Symbol(line, x, y)
                self.pos[x, y] = elem

    def __getitem__(self, pos: tuple[int, int]):
        return self.pos.get(pos, Empty())
    
    def items(self):
        return self.pos.items()
    
    def nums(self):
        return iter(self._nums)
    
    def mark_all(self):
        for pos, elem in self.items():
            elem.mark_adjacent(self)
        return (n for n in self.nums() if n.marked)

def compute(text):
    sc = Schematic(text)

    result = 0
    for n in sc.mark_all():
        result += n.value

    return(result)

compute(text)

def compute2(text):
    sc = Schematic(text)
    result = 0
    for _, elem in sc.items():
        if isinstance(elem, Symbol):
            result += elem.gear_ratio(sc)
    return result

compute2(text)

# %%

# %%

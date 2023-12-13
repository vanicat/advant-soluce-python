#%%

from dataclasses import dataclass
import io
from typing import Generator, Optional, Self

#%%


example = io.StringIO("""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
""")

SpecList = Optional[tuple[int, "SpecList"]]

def read_input(input:io.TextIOBase) -> Generator[tuple[str, SpecList], None, None]:
    for line in input.readlines():
        desc, nums = line.split()
        nums = [int(i) for i in nums.split(",")]
        spec = None
        for v in reversed(nums):
            spec = (v, spec)
        yield desc, spec

test_data = list(read_input(example))
# %%

def find_pos(desc, pos, n):
    seen = 0
    mandatory = 0
    for i in range(pos, len(desc)):
        if desc[i] == "?":
            seen += 1
            mandatory = 0
        elif desc[i] == "#":
            seen += 1
            mandatory += 1
        else:
            mandatory = 0
            seen = 0
        if seen >= n >= mandatory:
            if i + 1 >= len(desc) or desc[i + 1] != "#":
                yield i

def find_nb(desc, pos, rest) -> int:
    if rest == []:
        return 1
    total = 0
    yo = rest[1:]
    for i in find_pos(desc, pos, rest[0]):
        total += find_nb(desc, i+2, yo)
    return total

# %%

@dataclass(frozen=True)
class Position():
    current: Optional[int]
    pos: int
    rest: SpecList

    def read_c(self, c) -> Generator[Self, None, None]:
        if self.current is None:
            if c in [".", "?"]:
                yield self
            if c in ["#", "?"] and self.rest is not None:
                n, rest = self.rest
                yield Position(n, 1, rest)
        elif self.current == self.pos: # current is finished
            match c:
                case "." | "?":
                    yield Position(None, 0, self.rest)
                case "#":
                    pass
        else:
            match c:
                case ".":
                    pass
                case "?" | "#":
                    yield Position(self.current, self.pos + 1, self.rest)


def search_place(desc:str, spec:SpecList) -> int:
    state = { Position(None, 0, spec): 1 }

    for c in desc:
        new_state = {}
        for pos, mult in state.items():
            for next in pos.read_c(c):
                old = new_state.get(next, 0)
                new_state[next] = old + mult
        state = new_state


    score = 0
    for pos, nb in state.items():
        if (pos.current is None or pos.current == pos.pos) and pos.rest is None:
            score += nb
    return score

for desc, spec in test_data:
    print(search_place(desc, spec))
# %%

def total(data):
    score = 0
    
    for desc, spec in data:
        score += search_place(desc, spec)

    return score

print(total(test_data))

# %%


with open("input-day12.txt") as f:
    data = read_input(f)

    print(total(data))

# %%
def read_input2(input:io.TextIOBase) -> Generator[tuple[str, SpecList], None, None]:
    for line in input.readlines():
        desc, nums = line.split()
        nums = [int(i) for i in nums.split(",")]

        spec = None
        for _ in range(5):
            for v in reversed(nums):
                spec = (v, spec)
        
        yield "?".join([desc for _ in range(5)]), spec

    
with open("input-day12.txt") as f:
    data = read_input2(f)

    print(total(data))
# %%

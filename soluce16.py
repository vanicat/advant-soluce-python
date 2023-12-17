#%%

from enum import Enum, auto
import io
#%%

example = io.StringIO(""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
""")

class Direction(Enum):
    UPWARD=auto()
    DOWNWARD=auto()
    RIGHTWARD=auto()
    LEFTWARD=auto()

class Place:
    done:set[Direction]
    chr = "."
    def __init__(self):
        self.done = set()

    def arrive(self, dir:Direction) -> list[Direction]:
        if dir in self.done:
            return []
        self.done.add(dir)
        return self.depart(dir)

    def depart(self, dir:Direction) -> list[Direction]:
        return [dir]
    
    @property
    def active(self) -> bool:
        return self.done != set()
    
class MirrorDR(Place):
    chr = "/"
    def depart(self, dir: Direction) -> list[Direction]:
        match dir:
            case Direction.UPWARD:
                return [Direction.RIGHTWARD]
            case Direction.LEFTWARD:
                return [Direction.DOWNWARD]
            case Direction.RIGHTWARD:
                return [Direction.UPWARD]
            case Direction.DOWNWARD:
                return [Direction.LEFTWARD]


class MirrorDL(Place):
    chr = "\\"
    def depart(self, dir: Direction) -> list[Direction]:
        match dir:
            case Direction.UPWARD:
                return [Direction.LEFTWARD]
            case Direction.LEFTWARD:
                return [Direction.UPWARD]
            case Direction.RIGHTWARD:
                return [Direction.DOWNWARD]
            case Direction.DOWNWARD:
                return [Direction.RIGHTWARD]
    

class SplitV(Place):
    chr = "|"
    def depart(self, dir: Direction) -> list[Direction]:
        match dir:
            case Direction.UPWARD | Direction.DOWNWARD:
                return [dir]
            case Direction.LEFTWARD | Direction.RIGHTWARD:
                return [ Direction.UPWARD, Direction.DOWNWARD]
        assert False
    

class SplitH(Place):
    chr = "-"
    def depart(self, dir: Direction) -> list[Direction]:
        match dir:
            case Direction.UPWARD | Direction.DOWNWARD:
                return [Direction.LEFTWARD, Direction.RIGHTWARD]
            case Direction.LEFTWARD | Direction.RIGHTWARD:
                return [dir]
        assert False


Map = list[list[Place]]

def read_input(input:io.TextIOBase) -> Map:
    map:"Map" = []
    for line in input.readlines():
        new_line:list[Place] = []
        for c in line:
            match c:
                case ".":
                    new_line.append(Place())
                case "/":
                    new_line.append(MirrorDR())
                case "\\":
                    new_line.append(MirrorDL())
                case "-":
                    new_line.append(SplitH())
                case "|":
                    new_line.append(SplitV())
        map.append(new_line)
    return map

data_test = read_input(example)
def make_test_data():
    example = io.StringIO(""".|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....
""")
    return read_input(example)
# %%

def move(i, j, dir:Direction) -> tuple[int, int]:
    match dir:
        case Direction.UPWARD:
            return (i - 1, j)
        case Direction.LEFTWARD:
            return (i, j - 1)
        case Direction.RIGHTWARD:
            return (i, j + 1)
        case Direction.DOWNWARD:
            return (i + 1, j)
        
def step(i:int, j:int, dir:Direction, map:Map) -> list[tuple[int, int, Direction]]:
    elem = map[i][j]
    next_dirs = elem.arrive(dir)
    return [(*move(i, j, d), d) for d in next_dirs]

def activate(i: int, j:int, dir:Direction, map:Map) -> None:
    stack:list[tuple[int, int, Direction]] = [(i, j, dir)]
    while stack:
        i, j, dir = stack.pop()
        if 0 <= i < len(map) and 0 <= j < len(map[0]):
            stack.extend(step(i, j, dir, map))

data_test = make_test_data()
activate(0, 0, Direction.RIGHTWARD, data_test)

# %%
for li in data_test:
    for elem in li:
        print(elem.chr, end="")
    print()

print()

for li in data_test:
    for elem in li:
        if elem.active:
            print("#", end="")
        else:
            print(".", end="")
    print()

# %%

def score(map:Map) -> int:
    score = 0
    for line in map:
        for elem in line:
            if elem.active:
                score += 1
    return score    

# %%
with open("input-day16.txt") as f:
    data = read_input(f)
    activate(0, 0, Direction.RIGHTWARD, data)

    print(score(data))

# %%

def reinit(data:Map):
    for line in data:
        for elem in line:
            elem.done = set()

def values(data):
    for i in range(len(data)):
        reinit(data)
        activate(i, 0, Direction.RIGHTWARD, data)
        yield score(data)

        reinit(data)
        activate(i, len(data[0]) - 1, Direction.LEFTWARD, data)
        
        yield score(data)

    for j in range(len(data[0])):
        reinit(data)
        activate(0, j, Direction.DOWNWARD, data)
        yield score(data)

        reinit(data)
        activate(len(data) - 1, j, Direction.UPWARD, data)
        
        yield score(data)

print(max(values(data)))
# %%

#%% 
from functools import reduce
import io
#%%
test_input = io.StringIO("""LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""")

dest  = {
    "L": 0,
    "R": 1
}

def read_input(input:io.TextIOBase) -> tuple[str, dict[str, tuple[str, str]]]:
    path = input.readline().strip()
    input.readline()
    graph = {}
    for line in input.readlines():
        a, b = line.split(" = ")
        g, d = b[1:-2].split(", ")
        graph[a] = (g, d)
    return path, graph

test_path, test_graph = read_input(test_input)

# %%

def move(path:str, graph:dict[str, tuple[str, str]], start:str, stop:str) -> int:
    step = 0
    pos = start
    while True:
        for dir in path:
            if pos == stop:
                return step
            step += 1
            pos = graph[pos][dest[dir]]

move(test_path, test_graph, "AAA", "ZZZ")
# %%

with open("input-day8.txt") as input:
    path, graph = read_input(input)

move(path, graph, "AAA", "ZZZ")
# %%
# etape 2

test_input = io.StringIO("""LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
""")

test_path, test_graph = read_input(test_input)

def starting_node(graph:dict[str, tuple[str, str]]) -> list[str]:
    starting_node = [ n for n in graph if n[-1] == "A"]
    return starting_node

test_start = starting_node(test_graph)
test_start

# %%

def test_end(pos):
    for e in pos:
        if e[-1] != "Z":
            return False
    return True

def simple_move(path:str, graph:dict[str, tuple[str, str]], start, i):
    step = 0
    pos:str = start
    while True:
        dir = path[i]
        i += 1
        if i >= len(path):
            i = 0
        step += 1
        pos = graph[pos][dest[dir]]
        if pos[-1] == "Z":
            return step, pos, i
        

def make_graph2(path:str, graph:dict[str, tuple[str, str]]):
    graph2 = {}
    snode:list[str] = starting_node(graph)
    for start in snode:
        i = 0
        pos = start
        while (pos, i) not in graph2:
            step, new_pos, new_i = simple_move(path, graph, pos, i)
            graph2[(pos, i)] = (new_pos, new_i, step)
            pos = new_pos
            i = new_i
    return graph2

make_graph2(test_path, test_graph)

#%%

grp = make_graph2(path, graph)

def ppcm(a,b):
    p = a * b
    while(b != 0):
        a, b = b, a % b
    return p // a

nb = [v for _, _, v in grp.values()]

reduce(ppcm, nb)

# %%

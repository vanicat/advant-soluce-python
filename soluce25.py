#%%
from collections.abc import Generator
import networkx
import networkx.algorithms.connectivity.cuts as cuts

#%%
example_st = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""


with open("input-day25.txt") as f:
    problem_st = f.read()

#%%

def read_edge(st:str) -> Generator[tuple[str, str], None, None]:
    for line in st.split("\n"):
        if line == "":
            continue
        src, dests = line.split(": ")
        dests_list = dests.split()
        for dest in dests_list:
            yield src, dest

def read(st) -> networkx.Graph:
    G = networkx.Graph()
    G.add_edges_from(read_edge(st))
    return G

example = read(example_st)
problem = read(problem_st)

#%%
def solve(gr:networkx.Graph) -> tuple[int, int]:
    cut = networkx.minimum_edge_cut(gr)
    gr.remove_edges_from(cut)
    x, y = [len(c) for c in networkx.connected_components(gr)]
    return (x, y)

print("example: ", solve(example))
print("problem:", solve(problem))


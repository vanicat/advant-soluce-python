#%%
import io
#%%

example = io.StringIO("""rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7\n""")


def read_input(input:io.TextIOBase) -> list[str]:
    li = input.readline()
    li = li.rstrip()
    return li.split(",")
    
test_data = read_input(example)
print(test_data)
# %%
def hash(st):
    tot = 0
    for c in st:
        tot = ((tot + ord(c)) * 17) % 256
    return tot

assert hash("HASH") == 52

data_hash = [hash(st) for st in test_data]
assert data_hash == [30, 253, 97, 47, 14, 180, 9, 197, 48, 214, 231]

def compute(li:list[str]):
    return sum((hash(st) for st in li))

# %%
with open("input-day15.txt") as f:
    data = read_input(f)

    print(compute(data))
# %%

def init(instruction:list[str]) -> list[list[tuple[str, int]]]:
    boxes:list[list[tuple[str, int]]] = [[] for i in range(256)]
    for it in instruction:
        if it[-1] == "-":
            label = it[:-1]
            i = hash(label)
            box = boxes[i]
            for i, content in enumerate(box):
                if content[0] == label:
                    del box[i]
                    break
        else:
            lens = int(it[-1])
            label = it[:-2]
            i = hash(label)
            box = boxes[i]
            for i, content in enumerate(box):
                if content[0] == label:
                    box[i] = (label, lens)
                    label = None
                    break
            if label:
                box.append((label, lens))
    return boxes

assert init(test_data) == [[("rn", 1), ("cm", 2)], [], [], [("ot", 7), ("ab", 5), ("pc", 6)]] + [[]] * (256 - 4)

# %%

init(data)
# %%
def score(boxes):
    return sum((sum( ((nbox + 1) * (slot + 1) * lens[1] for slot, lens in enumerate(box)) ) for nbox, box in enumerate(boxes) ))

assert score(init(test_data)) == 145

print(score(init(data)))
# %%

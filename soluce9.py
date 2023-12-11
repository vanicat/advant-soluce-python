#%% 
from functools import reduce
import io
#%%
test_input = io.StringIO("""0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
""")

def read_input(input):
    return [[int(i) for i in line.split()] for line in input.readlines()]

test_data = read_input(test_input)
test_data
# %%
def step(line:list[int]) -> list[int]:
    return [line[i]-line[i-1] for i in range(1, len(line))]

def zerop(line:list[int]) -> bool:
    return all([i == 0 for i in line])

#%%
def extrapolate(line:list[int]) -> int:
    lines:list[list[int]] = [line]
    while not zerop(line):
        line = step(line)
        lines.append(line)
    predict = 0
    for line in reversed(lines):
        predict = line[-1] + predict
        
    return predict

extrapolate(test_data[0])
# %%
def score(data:list[list[int]], extrapolate=extrapolate):
    sum = 0
    for line in data:
        sum += extrapolate(line)
    return sum

score(test_data)

# %%
with open("input-day9.txt") as f:
    data = read_input(f)

print(score(data))
# %%
def extrapolate_prev(line:list[int]) -> int:
    lines:list[list[int]] = [line]
    while not zerop(line):
        line = step(line)
        lines.append(line)
    predict = 0
    for line in reversed(lines):
        predict = line[0] - predict
        
    return predict

extrapolate_prev(test_data[2])
# %%

score(test_data, extrapolate_prev)
# %%

with open("input-day9.txt") as f:
    data = read_input(f)

print(score(data, extrapolate_prev))
# %%

#%%

import math

#%%

test_input = ["Time:      7  15   30\n", "Distance:  9  40  200\n"]
with open("input-day6.txt") as f:
    input = f.readlines()

#%%

def read_line(line):
    return [int(x) for x in line.split()[1:]]

test_times = read_line(test_input[0])
test_dist = read_line(test_input[1])
times = read_line(input[0])
dist = read_line(input[1])

# %%

# attend x: vitesse x,  temps t-x parcours (t-x)*x = -x² + tx (on enleve d ensuite)  

def calc_dist(t, x):
    return x * (t - x)

def poly(t, d):
    a = -1
    b = t
    c = -d
    Δ = b*b - 4 * a * c
    x1 = (-b + math.sqrt(Δ))/(2 * a)
    x2 = (-b - math.sqrt(Δ))/(2 * a)

    x1_int = math.ceil(x1)
    if x1_int == x1:
        x1_int += 1
    
    x2_int = math.floor(x2)
    if x2_int == x2:
        x2_int -= 1
    
    return (x1_int, x2_int)

def soluce(times, dist):
    ranges = [poly(t, d) for t, d in zip(times, dist)]
    num = [x2 - x1 + 1 for x1, x2 in ranges]
    prod = 1
    for x in num:
        prod = prod * x
    return(prod)

print(soluce(test_times, test_dist))
print(soluce(times, dist))
print(dist)
print(soluce([56717999], [334113513502430]))

# %%

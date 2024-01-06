#%%

from typing import Optional, Self
from itertools import chain

#%%

def read_input(lines):
    seeds = [int(v) for v in lines[0][7:].split()]
    i = 2
    converter = []
    while i < len(lines):
        title = lines[i].rstrip()
        i += 1
        maps = []
        while i < len(lines) and lines[i] != "\n":
            maps.append([int(n) for n in lines[i].split()])
            assert len(maps[-1]) == 3, f"incorect line: {lines[i]}"
            i += 1
        i += 1
        converter.append((title, maps))
    return seeds, converter

with open("input-day5.txt") as input:
    input = read_input(input.readlines())

#%%
debug_string = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""".splitlines(True)
test_input = read_input(debug_string)

# %%

def decoupe_range(r:range, start, end) -> tuple[Optional[range], Optional[range], Optional[range]]:
    if r.start >= start:
        left = None
    else:
        left = range(r.start, min(r.stop, start))
    if r.stop <= end:
        right = None
    else:
        right = range(max(r.start, end), r.stop)
    if r.start < end and r.stop > start:
        midle = range(max(r.start, start), min(r.stop, end))
    else:
        midle = None
    return left, midle, right

decoupe_range(range(10, 20), 12, 21) 

#%%


class Feuille:
    est_feuille = True

    def __getitem__(self, n):
        return n

    def __str__(self):
        return "Feuille()"

    def find_range(self, titi):
        yield titi


class ABR:
    est_feuille = False

    def __init__(self, dest, source, length):
        self.source = source
        self.fin = source + length
        self.dest = dest
        self.left = Feuille()
        self.right = Feuille()

    def insert(self, dest, source, length):
        if source < self.source:
            if self.left.est_feuille:
                self.left = ABR(dest, source, length)
            else:
                self.left.insert(dest, source, length) # type: ignore
        else:
            if self.right.est_feuille:
                self.right = ABR(dest, source, length)
            else:
                self.right.insert(dest, source, length) # type: ignore

    def __getitem__(self, n):
        if n < self.source:
            return self.left[n]
        elif n >= self.fin:
            return self.right[n]
        else:
            return self.dest + (n - self.source)
        
    def __repr__(self):
        return f"ABR({self.left}, {self.source}, {self.fin}, {self.dest}, {self.right})"

    def find_range(self, titi:range):
        left, midle, right = decoupe_range(titi, self.source, self.fin)
        if left:
            yield from self.left.find_range(left)
        if midle:
            yield range(self[midle.start], self[midle.stop - 1] + 1)
        if right:
            yield from self.right.find_range(right)

import random


class Converter:
    def __init__(self, name:str, converteurs:list[list[int]]) -> None:
        name = name[:-5]
        self.source, self.dest = name.split("-to-")
        random.shuffle(converteurs)
        it = iter(converteurs)
        s, d, l = next(it)
        self.abr = ABR(s, d, l)
        for s, d, l in it:
            self.abr.insert(s, d, l)

    def __getitem__(self, n):
        return self.abr[n]
    
    def convert_list(self, li):
        result = []
        for value in li:
            result.append(self[value])

        return result
    
    def convert_range(self, r):
        return self.abr.find_range(r)

#%%

def make_converters(convert_desc):
    return [Converter(name, conv) for name, conv in convert_desc]

def apply_converters(seeds, converters):
    elems = seeds
    for c in converters:
        elems = c.convert_list(elems)
    return elems

def do_it(input):
    seeds, convert_desc = input
    converters = make_converters(convert_desc)
    return apply_converters([int(s) for s in seeds], converters)

#%%

print(do_it(test_input))

# %%

print(do_it(input))
print(min(do_it(input)))

# %%

seeds, convert_desc = test_input
converters = make_converters(convert_desc)
c0 = converters[0]

for i in range(50):
    assert c0[i] == i
for i, r in zip(range(50, 50+48), range(52, 52+48)):
    assert c0[i] == r
for i in range(50+48, 98):
    assert c0[i] == i
for i, r in zip(range(98, 98+2), range(50, 50+2)):
    assert c0[i] == r
for i in range(98+2, 200):
    assert c0[i] == i

# %%


toto = c0.convert_range(range(90, 120))

print(list(toto))


print(c0.convert_range(range(0, 30)))

# %%

def read_range(seeds):
    for i in range(0, len(seeds), 2):
        u = seeds[i]
        v = seeds[i+1]
        yield range(u, u+v)

list(read_range(seeds))

def do_it_range(input):
    seeds, convert_desc = input
    nyup = read_range(seeds)
    converters = make_converters(convert_desc)
    for c in converters:
        nyup = chain(*[c.convert_range(r) for r in nyup])

    return nyup

min([r.start for r in do_it_range(input)])

# %%



# %%

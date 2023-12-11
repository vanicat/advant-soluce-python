#%%

cards = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
cards_point = {
    cle: 13-value for value, cle in enumerate(cards)
}
def to_point(hand):
    return tuple((cards_point[c] for c in hand))

to_point("32T3K")

#%%
test_data = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
""".splitlines(True)

def read_data(data):
    spliting = [l.split() for l in data]
    return [(hand, int(value)) for hand, value in spliting]

read_data(test_data)
#%%

def find_type(hand, opt=None):
    in_order = sorted(hand)
    nums:list[int] = []
    x = in_order[0]
    n = 1
    for y in in_order[1:]:
        if x == y:
            n += 1
        else:
            nums.append(n)
            x = y
            n = 1
    nums.append(n)
    if nums[0] == 5:
        return 5
    if 4 in nums:
        return 4
    if 3 in nums and 2 in nums:
        return 3.5
    if 3 in nums:
        return 3
    if len(nums) == 3:
        return 2.5
    if len(nums) == 5:
        return 1
    return 2
    
def value(tirage):
    hand, _ = tirage
    return (find_type(hand), to_point(hand))
    
sorted(read_data(test_data), key=value)

# %%

def score(data, value=value):
    score = 0
    for r, tirage in enumerate(sorted(data, key=value)):
        score += (r+1) * tirage[1]
    return score

score(read_data(test_data))
# %%


with open("input-day7.txt") as f:
    data = f.readlines()
score(read_data(data))
# %%
cards2 = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
cards_point2 = {
    cle: 13-value for value, cle in enumerate(cards2)
}

def to_point2(hand):
    return tuple((cards_point2[c] for c in hand))


def find_type2(hand:str):
    joker = hand.count("J")
    in_order = sorted(hand)
    nums:list[int] = []
    x = in_order[0]
    n = 1
    for y in in_order[1:]:
        if x == y:
            n += 1
        else:
            if x != "J":
                nums.append(n)
            x = y
            n = 1
    if x != "J":
        nums.append(n)
    nums.sort(reverse=True)
    if len(nums) > 0:
        nums[0] += joker
    else:
        nums = [joker]
    if nums == [5]:
        return 5
    if nums == [4, 1]:
        return 4
    if nums == [3, 2]:
        return 3.5
    if nums == [3, 1, 1]:
        return 3
    if nums == [2, 2, 1]:
        return 2.5
    if nums == [2, 1, 1, 1]:
        return 2
    if nums == [1, 1, 1, 1, 1]:
        return 1
    assert False, f"problem with this hand {hand}"

def value2(tirage):
    hand, _ = tirage
    return (find_type2(hand), to_point2(hand))

sorted(read_data(test_data), key=value2)

# %%

score(read_data(test_data), value2)

# %%

score(read_data(data), value2)

# %%

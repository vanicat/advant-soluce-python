#%%

from dataclasses import dataclass
import io
import json
import re
from typing import Generator, Literal, TypedDict

#%%
example = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""

AttributeType = Literal["x", "m", "a", "s"]

@dataclass
class Rule:
    attribute:AttributeType
    gt: bool
    limit: int
    dest: str

Object = dict[AttributeType, int]

class Workflow:
    rules: list[Rule]
    last_rule: str

    def __init__(self, rules, last_rule):
        self.rules = rules
        self.last_rule = last_rule

    def apply(self, obj:Object) -> str:
        for rule in self.rules:
            v = obj[rule.attribute]
            if (rule.gt and v > rule.limit) or (not rule.gt and v < rule.limit):
                return rule.dest
            
        return self.last_rule
    
    def __repr__(self) -> str:
        return f"Wokflows({self.rules, self.last_rule})"
    

@dataclass
class Problem:
    workflows: dict[str, Workflow]
    objects: list[Object]

    def __getitem__(self, key:str):
        return self.workflows[key]
    
def read_attribute(str) -> AttributeType:
    if str not in "xmas":
        raise ValueError
    return str

def read_object(line:str) -> Object:
    split = line[1:-2].split(",")
    split_eq = (st.split("=") for st in split)
    return { read_attribute(name): int(value) for name, value in split_eq }


def read_workflows(line:str) -> tuple[str, Workflow]:
    name, rules_str, rest = re.split(r"[{}]", line)
    rules_list = rules_str.split(",")
    last_rule = rules_list.pop()

    matches = (
        re.match(r"([xmas])([><])([0-9]+):([a-zAR]+)", st) for st in rules_list
    )
    rules = [
        Rule(attribute=m.group(1), gt=m.group(2) == ">", limit = int(m.group(3)), dest=m.group(4)) # type: ignore
        for m in matches
    ]

    return(name, Workflow(rules, last_rule))

print(read_workflows("px{a<2006:qkq,m>2090:A,rfg}\n"))

def read_input(f) -> Problem:
    workflows = {}
    for line in f:
        if line == "\n":
            break
        name, w = read_workflows(line)
        workflows[name] = w

    objs = [ read_object(line) for line in f]
    return Problem(workflows, objs)

def read_exemple():
    return read_input(io.StringIO(example))

def apply_rules(pb:Problem, obj:Object) -> bool:
    cur_rule = "in"
    while cur_rule not in ["A", "R"]:
        cur_rule = pb[cur_rule].apply(obj)

    return cur_rule == "A"

example_pb = read_exemple()
print(example_pb)
print(apply_rules(example_pb, example_pb.objects[0]))
good_example = [obj for obj in example_pb.objects if apply_rules(example_pb, obj)]
print(good_example)

def score(pb):
    good = [obj for obj in pb.objects if apply_rules(pb, obj)]
    return sum(v["x"] + v["m"] + v["a"] + v["s"] for v in good)

print(score(example_pb))

# %%

with open("input-day19.txt") as f:
    problem = read_input(f)

print(score(problem))

# %%

import math

@dataclass
class Check_Range():
    start:int = 1
    end:int = 4000

    def __bool__(self) -> bool:
        return self.start <= self.end

    
    def __len__(self) -> int:
        return max(0, self.end - self.start + 1)
        
    
    def combine_rule(self, rule:Rule) -> "tuple[Check_Range, Check_Range]": 
        if rule.gt:
            match = Check_Range(start = rule.limit + 1, end = self.end)
            others = Check_Range(start = self.start, end = rule.limit)
        else:
            match = Check_Range(start = self.start, end = rule.limit - 1)
            others = Check_Range(start = rule.limit, end = self.end)
        
        return match, others

    
Check_limits = dict[AttributeType, Check_Range]


def apply_workflow_to_limits(limits: Check_limits, workflow:Workflow, stack:list[tuple[str, Check_limits]]) -> Generator[Check_limits, None, None]:
    for rule in workflow.rules:
        range = limits[rule.attribute]
        match, other = range.combine_rule(rule)
        if match and rule.dest != "R":
            new_limit = limits.copy()
            new_limit[rule.attribute] = match
            if rule.dest == "A":
                yield new_limit
            else:
                stack.append((rule.dest, new_limit))
        limits[rule.attribute] = other
        if not other:
            break
    else:   # python for else block are executed when there is no break.
        if workflow.last_rule == "A":
            yield limits
        elif workflow.last_rule != "R":
            stack.append((workflow.last_rule, limits))
    
    
def find_posibilities(pb:Problem) -> Generator[Check_limits, None, None]:
    stack:list[tuple[str, Check_limits]] = [("in", {"x": Check_Range(), "m": Check_Range(), "a": Check_Range(), "s": Check_Range()})]
    while stack:
        rule, limit = stack.pop()
        yield from apply_workflow_to_limits(limit, pb[rule], stack)


print(find_posibilities(example_pb))


def second_score(pb:Problem):
    score = 0
    for accepted in find_posibilities(pb):
        score += len(accepted["x"]) * len(accepted["m"]) * len(accepted["a"]) * len(accepted["s"])

    return score

print(second_score(example_pb))
# %%
print(second_score(problem))
# %%

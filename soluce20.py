#%%
from collections import deque
import io
from abc import ABC, abstractmethod
from typing import Any, Iterable, Literal

#%%

example = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""
example2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

pulse = bool

setup_type = tuple["Module", Iterable[str]]

class Problem:
    modules: "dict[str, Module]"
    queue: "deque[tuple[str, pulse, Module]]"
    setup_list: "list[setup_type]"
    num_high: int = 0
    num_low: int = 0
    debug: bool = False
    rx: "Rx"

    def __init__(self) -> None:
        self.modules = dict()
        self.queue = deque()
        self.setup_list = list()
        self.ignore = Ignore(self)

    def add_broadcaster(self, modules:Iterable[str]):
        br = Broadcaster("broadcaster", self)
        self["broadcaster"] = br
        self.setup_list.append((br, modules))

    def add_module(self, module:"Module", dest:Iterable[str]):
        self[module.name] = module
        self.setup_list.append((module, dest))

    def setup(self):
        self.rx = Rx("rx", self)
        self.add_module(self.rx, [])

        for m, dests in self.setup_list:
            m.setup(*dests)
            for d in dests:
                self[d].connect(m)

    def __getitem__(self, key:str) -> "Module":
        if key in self.modules:
            return self.modules[key]
        else:
            return self.ignore
    
    def __setitem__(self, key:str, item:"Module") -> None:
        self.modules[key] = item

    def add_pulse(self, src:str, m:"Module", level:pulse):
        if self.debug:
            sig = "high" if level else "low"
            print(f"{src} -{sig}-> {m.name}")

        self.queue.append((src, level, m))
        if level:
            self.num_high += 1
        else:
            self.num_low += 1

    def tick(self) -> None:
        src, level, module = self.queue.popleft()
        module.process_pulse(src, level)

    def button(self, num=1, debug=False) -> int:
        self.debug = debug
        self.num_high = 0
        self.num_low = 0
        for _ in range(num):
            self.add_pulse("button", self["broadcaster"], False)
            while self.queue:
                self.tick()
        return self.num_high * self.num_low


class Module(ABC):
    problem: Problem
    name: str 
    dests: "list[Module]"
    low_pulse: int = 0


    def __init__(self, name, problem:Problem) -> None:
        super().__init__()
        self.problem = problem
        self.name = name
        self.dests = []

    @abstractmethod
    def process_pulse(self, src:str, level:pulse) -> None:
        pass

    def setup(self, *args:str) -> None:
        self.dests = [self.problem[name] for name in args]

    def connect(self, m:"Module") -> None:
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"
    
    def send_all(self, level: pulse) -> None:
        for m in self.dests:
            self.problem.add_pulse(self.name, m, level)

class Ignore(Module):
    def __init__(self, pb:Problem) -> None:
        super().__init__("Ignore", pb)
        
    def process_pulse(self, src: str, level: pulse) -> None:
        pass

class Rx(Module):
    def __init__(self, name, problem: Problem) -> None:
        super().__init__(name, problem)
        self.low_pulse = 0

    def process_pulse(self, src: str, level: pulse) -> None:
        #print(self, "high" if level else "low")
        if not level:
            self.low_pulse += 1
            print(self, "low")
    
    def reset(self):
        self.low_pulse = 0

    def ok(self):
        return self.low_pulse >= 1


class Broadcaster(Module):
    def __init__(self, _:str, problem:Problem) -> None:
        super().__init__("broadcaster", problem)

    def process_pulse(self, src:str, level: pulse) -> None:
        self.send_all(level)


class FlipFlop(Module):
    state: bool

    def __init__(self, name:str, problem:Problem) -> None:
        super().__init__(name, problem)
        self.state = False

    def process_pulse(self, src:str, level: pulse) -> None:
        if level:
            return
        self.state = not self.state
        if self.state:
            send = True
        else:
            send = False
        self.send_all(send)


class Conjunction(Module):
    state: dict[str, pulse]
    dest: Module

    def __init__(self, name:str, problem: Problem) -> None:
        super().__init__(name, problem)
        self.state = {}
    
    def connect(self, m: Module) -> None:
        self.state[m.name] = False

    def process_pulse(self, src:str, level: pulse) -> None: #TODO
        self.state[src] = level
        send = not(all(self.state.values()))
        self.send_all(send)
        
#%%
def read_input(f:io.TextIOBase) -> Problem:
    pb = Problem()
    for line in f:
        if line == "\n":
            continue
        line = line.strip()
        name, dests = line.split(" -> ")

        match name[0]:
            case "b":
                _class = Broadcaster
            case "&":
                _class = Conjunction
            case "%":
                _class = FlipFlop
            case _:
                raise ValueError(f"strange line {line}")
        

        name = name[1:].rstrip()
        dests_name = dests.split(", ")
        
        module = _class(name, pb)
        pb.add_module(module, dests_name)

    pb.setup()
    return pb

#%%

def read_example(n=1) -> Problem:
    if n == 1:
        return read_input(io.StringIO(example))
    else:
        return read_input(io.StringIO(example2))

example_pb1 = read_example(1)
example_pb2 = read_example(2)

# %%
print(example_pb1.button(1000), example_pb2.button(1000))
# %%

with open("input-day20.txt") as f:
    problem = read_input(f)

print(problem.button(1000))
# %%

with open("input-day20.txt") as f:
    problem = read_input(f)

num = 0
while not problem.rx.ok():
    problem.rx.reset()
    problem.button()
    num += 1
    if num & 0b11111111111111 == 0:
        print(num)

print(num)
# %%

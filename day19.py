from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 19", "Part 1")
def solve_part1(lines: list):
    workflows, parts = parse_input(lines)
    sorter = Sorter(workflows)
    total = 0
    for part in parts:
        if sorter.accepted(part):
            total += part.rating()
    return total

@Runner("Day 19", "Part 2")
def solve_part2(lines: list):
    return -1

class Step:
    def __init__(self, s: str) -> None:
        self.test = None
        self.location = None
        if ":" in s:
            self.test, self.location = s.split(":")
        else:
            self.location = s
    
    def __repr__(self) -> str:
        return str((self.test, self.location))
    
    def execute(self, part: "Part") -> (bool, str):
        if self.test == None:
            return True, self.location
        return eval("part." + self.test), self.location

class Workflow:
    def __init__(self, line: str) -> None:
        i = line.index("{")
        self.id = line[:i]
        self.steps = []
        for s in line[i+1:len(line)-1].split(","):
            self.steps.append(Step(s))
            
    def __repr__(self) -> str:
        return str((self.id, self.steps))
    
    def result(self, part: "Part") -> str:
        for step in self.steps:
            done, loc = step.execute(part)
            if done:
                return loc
    
class Part:
    def __init__(self, line: str) -> None:
        pieces = line[1:len(line)-1].split(",")
        self.x = int(pieces[0].split("=")[1])
        self.m = int(pieces[1].split("=")[1])
        self.a = int(pieces[2].split("=")[1])
        self.s = int(pieces[3].split("=")[1])
        
    def __repr__(self) -> str:
        return str((self.x, self.m, self.a, self.s))
    
    def rating(self) -> int:
        return self.x + self.m + self.a + self.s

class Sorter:
    def __init__(self, workflows: list[Workflow]) -> None:
        self.wmap = {}
        for w in workflows:
            self.wmap[w.id] = w
        self.start = self.wmap["in"]
    
    def accepted(self, part: Part) -> bool:
        w = self.start
        while True:
            r = w.result(part)
            if r == "A":
                return True
            elif r == "R":
                return False
            else:
                w = self.wmap[r]

def parse_input(lines: list) -> (list[Workflow], list[Part]):
    idx = 0
    workflows = []
    while lines[idx] != "":
        workflows.append(Workflow(lines[idx]))
        idx += 1
    idx += 1
    parts = []
    for idx in range(idx, len(lines)):
        parts.append(Part(lines[idx]))
    return workflows, parts

# Part 1
input = read_lines("input/day19/input.txt")
sample = read_lines("input/day19/sample.txt")

value = solve_part1(sample)
assert(value == 19114)
value = solve_part1(input)
assert(value == 425811)

# Part 2
value = solve_part2(sample)
assert(value == -1)
value = solve_part2(input)
assert(value == -1)

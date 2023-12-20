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
    workflows, parts = parse_input(lines)
    sorter = Sorter(workflows)
    wf = sorter.workflow_by_id("in")
    total = 0
    init = PartPath({"x":(1,4000), "m":(1,4000), "a": (1,4000), "s": (1,4000)})
    for apath in wf.acceptable_paths(init, 0, sorter):
        total += apath.possibilities()
    return total

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
    
    def pass_values(self) -> (str, bool, int):
        return str(self.test[0]), self.test[1] == "<", int(self.test[2:])
    
    def fail_values(self) -> (str, bool, int):
        catg, less, value = self.pass_values()
        if less:
            value -= 1
        else:
            value += 1
        return catg, not less, value

class PartPath:
    def __init__(self, ranges: dict[str,tuple[int]]) -> None:
        self.ranges = ranges
        
    def __repr__(self) -> str:
        return str((self.xRange, self.mRange, self.aRange, self.sRange))
    
    def possibilities(self) -> int:
        total = 1
        for r in self.ranges.values():
            total *= r[1] - r[0] + 1
        return total
    
    def copy(self) -> "PartPath":
        return PartPath(self.ranges.copy())
    
    def adjustRange(self, catg: str, less: bool, value: int):
        r = self.ranges.get(catg)
        if less:
            self.ranges[catg] = (r[0], min(value-1, r[1]))
        else:
            self.ranges[catg] = (max(r[0], value+1), r[1])

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
            
    def acceptable_paths(self, input: PartPath, sidx: int, sorter: "Sorter") -> list[PartPath]:
        step = self.steps[sidx]
        if step.test == None:
            if step.location == "R":
                return []
            elif step.location == "A":
                return [input]
            else:
                return sorter.workflow_by_id(step.location).acceptable_paths(input, 0, sorter)
        else:
            paths = []
            if step.location != "R":
                p = input.copy()
                p.adjustRange(*step.pass_values())
                if step.location == "A":
                    paths.append(p)
                else:
                    paths.extend(sorter.workflow_by_id(step.location).acceptable_paths(p, 0, sorter))
            if sidx + 1 < len(self.steps):
                p = input.copy()
                p.adjustRange(*step.fail_values())
                paths.extend(self.acceptable_paths(p, sidx + 1, sorter))
            return paths
    
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
                
    def workflow_by_id(self, id: str) -> Workflow:
        return self.wmap[id]

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
assert(value == 167409079868000)
value = solve_part2(input)
assert(value == 131796824371749)

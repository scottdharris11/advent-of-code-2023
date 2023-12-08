import re
from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 8", "Part 1")
def solve_part1(lines: list):
    map = Map(lines)
    return map.steps()

@Runner("Day 8", "Part 2")
def solve_part2(lines: list):
    return -1

node_extract = re.compile("([A-Z]{3}) = \\(([A-Z]{3}), ([A-Z]{3})\\)")

class Map:
    def __init__(self, lines:str) -> None:
        self.directions = lines[0]
        self.nodes = {}
        for i in range(2, len(lines)):
            m = node_extract.match(lines[i]).groups()
            self.nodes[m[0]] = (m[1], m[2])
            
    def __repr__(self): 
        return str((self.directions, self.nodes))
    
    def steps(self) -> int:
        pos = "AAA"
        step = -1
        while pos != "ZZZ":
            step += 1
            dir = self.__direction(step)
            pos = self.__next_node(pos, dir)
        return step + 1
    
    def __direction(self, step: int) -> chr:
        idx = step
        while idx >= len(self.directions):
            idx -= len(self.directions)
        return self.directions[idx]
    
    def __next_node(self, node: str, dir: chr) -> str:
        n = self.nodes[node]
        if dir == 'L':
            return n[0]
        return n[1]

# Part 1
input = read_lines("input/day8-input.txt")
sample = read_lines("input/day8-sample.txt")
sample2 = read_lines("input/day8-sample2.txt")

value = solve_part1(sample)
assert(value == 2)
value = solve_part1(sample2)
assert(value == 6)
value = solve_part1(input)
assert(value == 22357)

# Part 2
value = solve_part2(sample)
assert(value == -1)
value = solve_part2(input)
assert(value == -1)

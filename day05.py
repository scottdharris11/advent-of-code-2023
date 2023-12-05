import sys
from utilities.data import read_lines, parse_integers
from utilities.runner import Runner

@Runner("Day 5", "Part 1")
def solve_part1(lines: list):
    a = parse_almanac(lines)
    min_location = sys.maxsize
    for seed in a.seeds:
        c = "seed"
        val = seed
        while c != "location":
            c, val = a.catg_number(c, val)
        if val < min_location:
            min_location = val
    return min_location

@Runner("Day 5", "Part 2")
def solve_part2(lines: list):
    return -1

class Almanac:
    def __init__(self) -> None:
        self.seeds = []
        self.catg_ranges = {}
    
    def parse_seeds(self, line: str):
        self.seeds = parse_integers(line.split(":")[1].strip(), " ")
    
    def parse_map(self, lines: list):
        c2c = lines[0].split(" ")[0].split("-")
        ranges = self.dest_target_range(c2c[0], c2c[2])
        for i in range(1, len(lines)):
            ranges.append(parse_integers(lines[i], " "))
        
    def dest_target_range(self, dest: str, target: str) -> list:
        if dest not in self.catg_ranges:
            self.catg_ranges[dest] = {}
        if target not in self.catg_ranges[dest]:
            self.catg_ranges[dest][target] = []
        return self.catg_ranges[dest][target]
    
    def catg_number(self, dest: str, val: int) -> (str, int):
        c = list(self.catg_ranges[dest].keys())[0]
        ranges = self.catg_ranges[dest][c]
        for r in ranges:
            begin = r[1]
            end = r[1] + r[2] - 1
            if val >= begin and val <= end:
                return c, r[0] + val - r[1]
        return c, val

def parse_almanac(lines: list) -> Almanac:
    a = Almanac()
    a.parse_seeds(lines[0])
    
    start, end = 2, 2
    for i in range(2, len(lines)):
        end += 1
        if lines[i] == "":
            a.parse_map(lines[start:end-1])
            start, end = i+1, i+1
    a.parse_map(lines[start:end])
    return a

# Part 1
input = read_lines("input/day5-input.txt")
sample = read_lines("input/day5-sample.txt")

value = solve_part1(sample)
assert(value == 35)
value = solve_part1(input)
assert(value == 579439039)

# Part 2
value = solve_part2(sample)
assert(value == -1)
value = solve_part2(input)
assert(value == -1)

from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 23", "Part 1")
def solve_part1(lines: list):
    return -1

@Runner("Day 23", "Part 2")
def solve_part2(lines: list):
    return -1

# Part 1
input = read_lines("input/day23/input.txt")
sample = read_lines("input/day23/sample.txt")

value = solve_part1(sample)
assert(value == -1)
value = solve_part1(input)
assert(value == -1)

# Part 2
value = solve_part2(sample)
assert(value == -1)
value = solve_part2(input)
assert(value == -1)
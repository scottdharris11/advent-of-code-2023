from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 15", "Part 1")
def solve_part1(lines: list):
    total = 0
    for instruction in lines[0].split(","):
        total += hash_alog(instruction)
    return total

@Runner("Day 15", "Part 2")
def solve_part2(lines: list):
    return -1

def hash_alog(s: str) -> int:
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256
    return h

# Part 1
input = read_lines("input/day15/input.txt")
sample = read_lines("input/day15/sample.txt")

assert(hash_alog("HASH") == 52)

value = solve_part1(sample)
assert(value == 1320)
value = solve_part1(input)
assert(value == 510792)

# Part 2
value = solve_part2(sample)
assert(value == -1)
value = solve_part2(input)
assert(value == -1)

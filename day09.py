from utilities.data import read_lines, parse_integers
from utilities.runner import Runner

@Runner("Day 9", "Part 1")
def solve_part1(lines: list):
    total = 0
    for line in lines:
        total += next_value(parse_integers(line, " "))
    return total

@Runner("Day 9", "Part 2")
def solve_part2(lines: list):
    total = 0
    for line in lines:
        total += prev_value(parse_integers(line, " "))
    return total

def next_value(values: list[int]) -> int:
    d, allzeroes = diffs(values)
    if allzeroes:
        return 0
    return values[-1] + next_value(d)

def prev_value(values: list[int]) -> int:
    d, allzeroes = diffs(values)
    if allzeroes:
        return 0
    return values[0] - prev_value(d)      

def diffs(values: list[int]) -> (list[int], bool):
    diffs = []
    allzeroes = True
    for i in range(len(values)-1):
        d = values[i+1] - values[i]
        diffs.append(d)
        if values[i+1] != 0 or values[i] != 0:
            allzeroes = False
    return diffs, allzeroes

# Part 1
input = read_lines("input/day9-input.txt")
sample = read_lines("input/day9-sample.txt")

value = solve_part1(sample)
assert(value == 114)
value = solve_part1(input)
assert(value == 1696140818)

# Part 2
value = solve_part2(sample)
assert(value == 2)
value = solve_part2(input)
assert(value == 1152)

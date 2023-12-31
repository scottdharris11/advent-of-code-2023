from utilities.data import read_lines, parse_integers
from utilities.runner import Runner

@Runner("Day 9", "Part 1")
def solve_part1(lines: list):
    total = 0
    for line in lines:
        total += prev_next_values(parse_integers(line, " "))[1]
    return total

@Runner("Day 9", "Part 2")
def solve_part2(lines: list):
    total = 0
    for line in lines:
        total += prev_next_values(parse_integers(line, " "))[0]
    return total

def prev_next_values(values: list[int]) -> (int, int):
    diffs = []
    allzeroes = True
    for i in range(len(values)-1):
        d = values[i+1] - values[i]
        diffs.append(d)
        if values[i+1] != 0 or values[i] != 0:
            allzeroes = False
    if allzeroes:
        return 0, 0
    po, pn = prev_next_values(diffs)
    return values[0] - po,  values[-1] + pn

# Part 1
input = read_lines("input/day09/input.txt")
sample = read_lines("input/day09/sample.txt")

value = solve_part1(sample)
assert(value == 114)
value = solve_part1(input)
assert(value == 1696140818)

# Part 2
value = solve_part2(sample)
assert(value == 2)
value = solve_part2(input)
assert(value == 1152)

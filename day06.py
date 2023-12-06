from utilities.data import read_lines, parse_integers
from utilities.runner import Runner

@Runner("Day 6", "Part 1")
def solve_part1(lines: list):
    time = parse_integers(lines[0].split(":")[1].strip(), " ")
    dist = parse_integers(lines[1].split(":")[1].strip(), " ")
    value = 1
    for i in range(len(time)):
        value *= record_breaking_options(time[i], dist[i])
    return value

@Runner("Day 6", "Part 2")
def solve_part2(lines: list):
    time = int(lines[0].split(":")[1].replace(" ", ""))
    dist = int(lines[1].split(":")[1].replace(" ", ""))
    return record_breaking_options(time, dist)

# find minimum holding time and maximum holding time from the
# two ends...all options in between will break record
def record_breaking_options(time: int, record: int) -> int:
    min_hold = 1
    mills = time - 1
    while True:
        if min_hold * mills > record:
            break
        min_hold += 1
        mills -= 1
        
    max_hold = time - 1
    mills = 1
    while True:
        if max_hold * mills > record:
            break
        max_hold -= 1
        mills += 1
    
    return max_hold - min_hold + 1

# Part 1
input = read_lines("input/day6-input.txt")
sample = read_lines("input/day6-sample.txt")

value = solve_part1(sample)
assert(value == 288)
value = solve_part1(input)
assert(value == 625968)

# Part 2
value = solve_part2(sample)
assert(value == 71503)
value = solve_part2(input)
assert(value == 43663323)

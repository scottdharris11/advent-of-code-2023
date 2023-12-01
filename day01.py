import re
from re import Pattern
from utilities.data import read_lines
from utilities.runner import Runner

digit_words = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

@Runner("Day 1", "Part 1")
def solve_part1(lines: list):
    total = 0
    for line in lines:
        first = -1
        last = -1
        for c in line:
            if c.isdigit():
                if first == -1:
                    first = c
                    last = first
                else:
                    last = c
        total += int("%s%s" % (first, last))
    return total
    
@Runner("Day 1", "Part 2")
def solve_part2(lines: list):
    total = 0
    for line in lines:
        first = -1
        last = -1
        for i in range(len(line)):
            digit = -1
            if line[i].isdigit():
                digit = line[i]
            else:
                for k in digit_words.keys():
                    if line[i:i+len(k)] == k:    
                        digit = digit_words[k]
                        break
            if digit != -1:
                if first == -1:
                    first = digit
                    last = first
                else:
                    last = digit
        total += int("%s%s" % (first, last))
    return total

@Runner("Day 1", "Part 1")
def solve_part1_re(lines: list):
    regex = re.compile("([0-9]{1})")
    total = 0
    for line in lines:
        total += regex_solve(regex, line)
    return total

@Runner("Day 1", "Part 2")
def solve_part2_re(lines: list):
    regex = re.compile("(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))")
    total = 0
    for line in lines:
        total += regex_solve(regex, line)
    return total

def regex_solve(regex: Pattern, line: str):
    matches = tuple(regex.findall(line))
    first = digit(matches[0])
    last = digit(matches[len(matches)-1])
    return int("".join([first, last]))

def digit(s: str):
    if s in digit_words:
        return digit_words[s]
    return s

# Part 1
part1_sample = [
    "1abc2",
    "pqr3stu8vwx",
    "a1b2c3d4e5f",
    "treb7uchet",
]

value = solve_part1(part1_sample)
assert(value == 142)
value = solve_part1(read_lines("input/day1-input.txt"))
assert(value == 54331)

value = solve_part1_re(part1_sample)
assert(value == 142)
value = solve_part1_re(read_lines("input/day1-input.txt"))
assert(value == 54331)

# Part 2
part2_sample = [
    "two1nine",
    "eightwothree",
    "abcone2threexyz",
    "xtwone3four",
    "4nineeightseven2",
    "zoneight234",
    "7pqrstsixteen",
]

value = solve_part2(part2_sample)
assert(value == 281)
value = solve_part2(read_lines("input/day1-input.txt"))
assert(value == 54518)

value = solve_part2_re(part2_sample)
assert(value == 281)
value = solve_part2_re(read_lines("input/day1-input.txt"))
assert(value == 54518)

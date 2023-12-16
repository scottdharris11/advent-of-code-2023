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
    regex = re.compile("([0-9])")
    total = 0
    for line in lines:
        total += calibration(regex, line)
    return total

@Runner("Day 1", "Part 2")
def solve_part2(lines: list):
    regex = re.compile("(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))")
    total = 0
    for line in lines:
        total += calibration(regex, line)
    return total

def calibration(regex: Pattern, line: str):
    matches = tuple(regex.findall(line))
    first = digit(matches[0])
    last = digit(matches[-1])
    return int(first+last)

def digit(s: str):
    if s in digit_words:
        return digit_words[s]
    return s

# Part 1
input = read_lines("input/day01/input.txt")
sample = [
    "1abc2",
    "pqr3stu8vwx",
    "a1b2c3d4e5f",
    "treb7uchet",
]

value = solve_part1(sample)
assert(value == 142)
value = solve_part1(input)
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
value = solve_part2(input)
assert(value == 54518)

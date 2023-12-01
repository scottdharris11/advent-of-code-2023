from utilities.data import read_lines
from utilities.runner import Runner

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
    num_words = {
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
    
    total = 0
    for line in lines:
        first = -1
        last = -1
        for i in range(len(line)):
            digit = -1
            if line[i].isdigit():
                digit = line[i]
            else:
                for k in num_words.keys():
                    if line[i:i+len(k)] == k:    
                        digit = num_words[k]
                        break
            if digit != -1:
                if first == -1:
                    first = digit
                    last = first
                else:
                    last = digit
        total += int("%s%s" % (first, last))
    return total

# Part 1
value = solve_part1([
    "1abc2",
    "pqr3stu8vwx",
    "a1b2c3d4e5f",
    "treb7uchet",
])
assert(value == 142)
value = solve_part1(read_lines("input/day1-input.txt"))
assert(value == 54331)

# Part 2
value = solve_part2([
    "two1nine",
    "eightwothree",
    "abcone2threexyz",
    "xtwone3four",
    "4nineeightseven2",
    "zoneight234",
    "7pqrstsixteen",
])
assert(value == 281)
value = solve_part2(read_lines("input/day1-input.txt"))
assert(value == 54518)


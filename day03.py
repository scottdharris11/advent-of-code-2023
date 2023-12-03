from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 3", "Part 1")
def solve_part1(lines: list):
    parts = locate_parts(lines)
    total = 0
    for part in parts:
        total += part.number
    return total

@Runner("Day 3", "Part 2")
def solve_part2(lines: list):
    parts = locate_parts(lines)
    total = 0
    line_index = -1
    for line in lines:
        line_index += 1
        char_index = -1
        for c in line:
            char_index += 1
            if c == '*':
                total += gear_ratio(parts, line_index, char_index)
    return total

def locate_parts(lines: list):
    parts = []
    line_index = -1
    for line in lines:
        line_index += 1
        begin = -1
        end = -1
        char_index = -1
        for c in line:
            char_index += 1
            if c.isdigit():
                if begin == -1:
                    begin = char_index
                end = char_index
            else:
                if begin >= 0:
                    part = part_number(lines, line_index, begin, end)
                    if part > 0:
                        parts.append(Part(part, line_index, begin, end))
                    begin = -1
                    end = -1
        if begin >= 0:
            part = part_number(lines, line_index, begin, end)
            if part > 0:
                parts.append(Part(part, line_index, begin, end))
    return parts

def part_number(lines: list, y: int, begin: int, end: int):
    for yoffset in [-1, 0, 1]:
        for x in range(begin-1, end+2):
            if is_symbol(lines, y+yoffset, x):
                part = int(lines[y][begin:end+1])
                return part
    return 0

def is_symbol(lines: list, y: int, x: int):
    if y < 0 or y >= len(lines):
        return False
    if x < 0 or x >= len(lines[0]):
        return False
    if lines[y][x].isdigit() or lines[y][x] == ".":
        return False
    return True

def gear_ratio(parts: list, y: int, x: int):
    adjancent_parts = set()
    for yoffset in [-1, 0, 1]:
        for xoffset in range(x-1, x+2):
            for part in parts:
                if part.line == y+yoffset and part.begin <= xoffset and part.end >= xoffset:
                    adjancent_parts.add(part.number)
    
    if len(adjancent_parts) == 2:
        ratio = 1
        for p in adjancent_parts:
            ratio *= p
        return ratio
    return 0

class Part:
    def __init__(self, number, line, begin, end) -> None:
        self.number = number
        self.line = line
        self.begin = begin
        self.end = end
    
# Part 1
input = read_lines("input/day3-input.txt")
sample = [
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598..",    
]

value = solve_part1(sample)
assert(value == 4361)
value = solve_part1(input)
assert(value == 546312)

# Part 2
value = solve_part2(sample)
assert(value == 467835)
value = solve_part2(input)
assert(value == 87449461)

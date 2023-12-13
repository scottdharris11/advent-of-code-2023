from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 13", "Part 1")
def solve_part1(lines: list):
    patterns = parse_patterns(lines)
    total = 0
    for p in patterns:
        total += p.outside_total()
    return total

@Runner("Day 13", "Part 2")
def solve_part2(lines: list):
    return -1

class Pattern:
    def __init__(self, lines) -> None:
        self.rows = lines
        self.cols = self.__columns(lines)
        
    def outside_total(self) -> int:
        vertical = self.__outside_reflection(self.cols)
        horitzontal = self.__outside_reflection(self.rows)
        t = vertical
        t += horitzontal * 100
        return t
    
    def any_total(self) -> int:
        vertical = self.__any_reflection(self.cols)
        horitzontal = self.__any_reflection(self.rows)
        t = vertical
        t += horitzontal * 100
        return t
            
    def __columns(self, rows: list[str]) -> list[str]:
        cols = []
        for i in range(len(rows[0])):
            cols.append("")
            for r in rows:
                cols[i] += r[i]
        return cols
        
    def __outside_reflection(self, rows: list[str]) -> int:
        l = len(rows)
        for i in range(1, l, 2):
            if self.__reflection(rows[i:]):
                return int((l-i) / 2) + i
        for i in range(1, l, 2):
            if self.__reflection(rows[:l-i]):
                return int((l-i) / 2)
        return 0
    
    def __any_reflection(self, rows: list[str]) -> int:
        for i, row in enumerate(rows):
            for m in range(len(rows)-1, i+1, -1):
                if row == rows[m]:
                    if self.__reflection(rows[i:m+1]):
                        return int((m - i + 1) / 2) + 1
        return 0
                    
    def __reflection(self, lines: list[str]) -> bool:
        t = 0
        b = len(lines) - 1
        while t < b:
            if lines[t] != lines[b]:
                return False
            t += 1
            b -= 1
        return True

def parse_patterns(lines: list[str]) -> list[Pattern]:
    lines.append("")
    patterns = []
    pStart = 0
    for i, line in enumerate(lines):
        if line == "":
            patterns.append(Pattern(lines[pStart:i]))
            pStart = i+1
            continue
    return patterns

# Part 1
input = read_lines("input/day13-input.txt")
sample = read_lines("input/day13-sample.txt")

value = solve_part1(sample)
assert(value == 405)
value = solve_part1(input)
assert(value == 30575)

# Part 2
value = solve_part2(sample)
assert(value == -1)
value = solve_part2(input)
assert(value == -1)

from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 13", "Part 1")
def solve_part1(lines: list):
    patterns = parse_patterns(lines)
    total = 0
    for p in patterns:
        total += p.value(False)
    return total

@Runner("Day 13", "Part 2")
def solve_part2(lines: list):
    patterns = parse_patterns(lines)
    total = 0
    for p in patterns:
        total += p.value(True)
    return total

class Pattern:
    def __init__(self, lines) -> None:
        self.rows = lines
        self.cols = self.__columns(lines)
        
    def value(self, smudges: bool) -> int:
        vertical = self.__reflection_point(self.cols)
        horitzontal = self.__reflection_point(self.rows)
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
        
    def __reflection_point(self, rows: list[str]) -> int:
        l = len(rows)
        for i in range(1, l, 2):
            if self.__reflection(rows[i:]):
                return int((l-i) / 2) + i
        for i in range(1, l, 2):
            if self.__reflection(rows[:l-i]):
                return int((l-i) / 2)
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
    input = lines[:]
    input.append("")
    patterns = []
    pStart = 0
    for i, line in enumerate(input):
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
assert(value == 400)
value = solve_part2(input)
assert(value == -1)

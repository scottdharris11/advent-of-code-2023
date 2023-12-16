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
    def __init__(self, lines, id) -> None:
        self.id = id
        self.rows = []
        for line in lines:
            self.rows.append(list(line))
        self.cols = self.__columns(self.rows)
        
    def value(self, smudges: bool) -> int:
        vertical = 0
        horitzontal = 0
        if smudges:
            row_count = len(self.rows)
            col_count = len(self.rows[0])
            for i in range(row_count):
                for j in range(col_count):
                    orig = self.rows[i][j]
                    replace = "."
                    if orig == ".":
                        replace = "#"
                    
                    self.rows[i][j] = replace
                    self.cols[j][i] = replace
                    vertical = self.__reflection_point(self.cols, j)
                    horitzontal = self.__reflection_point(self.rows, i)
                    self.rows[i][j] = orig
                    self.cols[j][i] = orig
                    if horitzontal > 0 or vertical > 0:
                        break
                if horitzontal > 0 or vertical > 0:
                    break
        else:
            vertical = self.__reflection_point(self.cols, None)
            horitzontal = self.__reflection_point(self.rows, None)
        t = vertical
        t += horitzontal * 100
        return t
                
    def __columns(self, rows: list[list[chr]]) -> list[str]:
        cols = []
        for i in range(len(rows[0])):
            c = []
            for r in rows:
                c.append(r[i])
            cols.append(c)
        return cols
        
    def __reflection_point(self, rows: list[str], smudgeIdx: int) -> int:
        l = len(rows)
        for i in range(1, l, 2):
            if self.__reflection(rows[i:]) and self.__inrange((i, l-1), smudgeIdx):
                return int((l-i) / 2) + i
        for i in range(1, l, 2):
            if self.__reflection(rows[:l-i]) and self.__inrange((0, l-i-1), smudgeIdx):
                return int((l-i) / 2)
        return 0
    
    def __inrange(self, r: tuple[int], idx: int) -> True:
        if idx == None:
            return True
        return idx >= r[0] and idx <= r[1]
    
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
    id = 1
    for i, line in enumerate(input):
        if line == "":
            patterns.append(Pattern(lines[pStart:i], id))
            pStart = i+1
            id += 1
            continue
    return patterns

# Part 1
input = read_lines("input/day13/input.txt")
sample = read_lines("input/day13/sample.txt")

value = solve_part1(sample)
assert(value == 405)
value = solve_part1(input)
assert(value == 30575)

# Part 2
value = solve_part2(sample)
assert(value == 400)
value = solve_part2(input)
assert(value == 37478)

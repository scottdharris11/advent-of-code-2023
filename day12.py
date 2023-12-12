from utilities.data import read_lines, parse_integers
from utilities.runner import Runner

@Runner("Day 12", "Part 1")
def solve_part1(lines: list):
    total = 0
    for line in lines:
        s = line.split(" ")
        total += possibilities(Record(s[0], parse_integers(s[1], ",")))
    return total

@Runner("Day 12", "Part 2")
def solve_part2(lines: list):
    return -1

class Record:
    def __init__(self, mask: str, pattern: list[int]) -> None:
        self.mask = mask
        self.pattern = pattern
    
    def __repr__(self):
        return str((self.mask, self.pattern))

def possibilities(r: Record) -> int:
    #print(r)
    unknown = r.mask.count('?')
    tofill = sum(r.pattern) - r.mask.count('#')
    if tofill == 0:
        return 0
    placements = []
    for i in range(unknown-tofill+1):
        fill(r, tofill, unknown, tuple(), i, placements)
    #print(placements)
    return len(placements)

def fill(r: Record, tofill: int, unknown: int, filled: tuple[int], start: int, placements: list):
    f = list(filled)
    f.append(unknownStrIndex(r.mask, start))
    if not possible(r, f):
        return
    if len(f) == tofill:
        placements.append(tuple(f))
        return
    for i in range(start+1, unknown):
        fill(r, tofill, unknown, tuple(f), i, placements)
        
def unknownStrIndex(mask: str, i: int) -> int:
    count = 0
    for si, c in enumerate(mask):
        if c == '?':
            if count == i:
                return si
            count += 1

def possible(r: Record, placement: tuple[int]) -> bool:
    uCnt = 0
    uIdx = 0
    placed = 0
    for i, c in enumerate(r.mask):
        if c == '?':
            if placed == len(placement):
                return uCnt <= r.pattern[uIdx]
            c = "."
            if i in placement:
                placed += 1
                c = "#"
        if c == "#":
            uCnt += 1
        else:
            if uCnt == 0:
                continue
            if uCnt != r.pattern[uIdx]:
                return False
            uIdx += 1
            uCnt = 0
            if placed == len(placement):
                return True
    return uCnt == r.pattern[-1]
            

# Part 1
input = read_lines("input/day12-input.txt")
sample = read_lines("input/day12-sample.txt")

value = solve_part1(sample)
assert(value == 21)
#value = solve_part1(["#..??####??? 1,4"])
value = solve_part1(input)
assert(value > 7218)
assert(value < 7851)

# Part 2
value = solve_part2(sample)
assert(value == -1)
value = solve_part2(input)
assert(value == -1)

from utilities.data import read_lines, parse_integers
from utilities.runner import Runner

@Runner("Day 12", "Part 1")
def solve_part1(lines: list):
    total = 0
    for line in lines:
        s = line.split(" ")
        total += possibilities(s[0], parse_integers(s[1], ","))
    return total

@Runner("Day 12", "Part 2")
def solve_part2(lines: list):
    return -1

def possibilities(mask: str, pattern: list[int]) -> int:
    unknown = mask.count('?')
    tofill = sum(pattern) - mask.count('#')
    placements = []
    for i in range(unknown-tofill+1):
        fill(mask, tofill, unknown, tuple(), i, placements)
    p = 0
    for placement in placements:
        if possible(mask, placement, pattern):
            p += 1
    return p

def fill(mask: str, tofill: int, unknown: int, filled: tuple[int], start: int, placements: list):
    f = list(filled)
    f.append(unknownStrIndex(mask, start))
    if len(f) == tofill:
        placements.append(tuple(f))
        return
    for i in range(start+1, unknown):
        fill(mask, tofill, unknown, tuple(f), i, placements)
        
def unknownStrIndex(mask: str, i: int) -> int:
    count = 0
    for si, c in enumerate(mask):
        if c == '?':
            if count == i:
                return si
            count += 1

def possible(mask: str, unknown: tuple[int], pattern: list[int]) -> bool:
    uCnt = 0
    uIdx = 0
    for i, c in enumerate(mask):
        if c == '?':
            c = "."
            if i in unknown:
                c = "#"
        if c == "#":
            uCnt += 1
        else:
            if uCnt == 0:
                continue
            if uCnt != pattern[uIdx]:
                return False
            uIdx += 1
            uCnt = 0
            if uIdx == len(pattern):
                return True
    return uCnt == pattern[-1]
            

# Part 1
input = read_lines("input/day12-input.txt")
sample = read_lines("input/day12-sample.txt")

value = solve_part1(sample)
assert(value == 21)
value = solve_part1(input)
assert(value > 7218)

# Part 2
value = solve_part2(sample)
assert(value == -1)
value = solve_part2(input)
assert(value == -1)

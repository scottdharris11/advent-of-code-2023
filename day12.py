from utilities.data import read_lines, parse_integers
from utilities.runner import Runner

@Runner("Day 12", "Part 1")
def solve_part1(lines: list):
    total = 0
    for line in lines:
        s = line.split(" ")
        r = Record(s[0], parse_integers(s[1], ","))
        total += possibilities(r)
    return total

@Runner("Day 12", "Part 2")
def solve_part2(lines: list):
    total = 0
    for line in lines:
        s = line.split(" ")
        r = Record(s[0], parse_integers(s[1], ","))
        #r.unfold()
        possible = possibilities(r)
        total += possible
    return total

class Record:
    def __init__(self, mask: str, pattern: list[int]) -> None:
        self.mask = mask
        self.pattern = pattern
        self.unknown = mask.count('?')
        self.damagedtofill = sum(pattern) - mask.count('#')
    
    def __repr__(self):
        return str((self.mask, self.pattern))
    
    def unknownIndex(self, i: int) -> int:
        count = 0
        for si, c in enumerate(self.mask):
            if c == '?':
                if count == i:
                    return si
                count += 1
    
    def unfold(self) -> None:
        nmask = self.mask
        npattern = self.pattern[:]
        for _ in range(4):
            nmask += "?"
            nmask += self.mask
            npattern.extend(self.pattern[:])
        self.mask = nmask
        self.pattern = npattern
        self.unknown = nmask.count('?')
        self.damagedtofill = sum(npattern) - nmask.count('#')

def possibilities(r: Record) -> int:
    if r.damagedtofill == 0:
        return 1
    #print(r)
    placements = []
    for i in range(r.unknown-r.damagedtofill+1):
        fill(r, tuple(), i, placements)
    #print(placements)
    return len(placements)

def fill(r: Record, filled: tuple[int], idx: int, placements: list):
    f = list(filled)
    f.append(r.unknownIndex(idx))
    if not possible(r, f):
        return
    if len(f) == r.damagedtofill:
        placements.append(tuple(f))
        return
    for i in range(idx+1, r.unknown):
        fill(r, tuple(f), i, placements)

def possible(r: Record, placement: tuple[int]) -> bool:
    print((r, placement))
    if len(placement) > r.damagedtofill:
        return False
    damageCnt, damageIdx, placed = 0, 0, 0
    for i, c in enumerate(r.mask):
        if c == '?':
            if placed == len(placement) and placed < r.damagedtofill:
                return damageCnt <= r.pattern[damageIdx]
            c = "."
            if i in placement:
                placed += 1
                c = "#"
        if c == "#":
            damageCnt += 1
        else:
            if damageCnt == 0:
                continue
            if damageCnt != r.pattern[damageIdx]:
                return False
            damageIdx += 1
            damageCnt = 0
    return damageCnt == 0 or damageCnt == r.pattern[-1]

# Part 1
input = read_lines("input/day12/input.txt")
sample = read_lines("input/day12/sample.txt")

value = solve_part1(sample)
assert(value == 21)
value = solve_part1(input)
assert(value == 7221)

# Part 2
value = solve_part2(sample)
assert(value == 525152)
value = solve_part2(input)
assert(value == -1)

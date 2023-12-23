from utilities.data import read_lines, parse_integers
from utilities.runner import Runner

@Runner("Day 12", "Part 1")
def solve_part1(lines: list):
    total = 0
    for line in lines:
        s = line.split(" ")
        r = Record(s[0], parse_integers(s[1], ","))
        p = possibilities(r.mask, r.pattern, 0)
        total += p
    return total

@Runner("Day 12", "Part 2")
def solve_part2(lines: list):
    total = 0
    for line in lines:
        s = line.split(" ")
        r = Record(s[0], parse_integers(s[1], ","))
        #r.unfold()
        possible = possibilities(r.mask, r.pattern, 0)
        total += possible
    return total

class Record:
    def __init__(self, mask: str, pattern: list[int]) -> None:
        self.mask = mask
        self.pattern = pattern
    
    def __repr__(self):
        return str((self.mask, self.pattern))
        
    def unfold(self) -> None:
        nmask = self.mask
        npattern = self.pattern[:]
        for _ in range(4):
            nmask += "?"
            nmask += self.mask
            npattern.extend(self.pattern[:])
        self.mask = nmask
        self.pattern = npattern

def possibilities(mask: str, pattern: list[int], prev_digits: int) -> int:
    done = len(pattern) == 0 or (len(pattern) == 1 and pattern[0] == 0)
    if mask == "":
        return 1 if done else 0
    if done:
        return 1 if mask.count("#") == 0 else 0
    
    if pattern[0] == 0 and mask[0] == "#":
        return 0
    if pattern[0] == 0 and (mask[0] == "." or mask[0] == "?"):
        return possibilities(mask[1:], pattern[1:], 0)
    
    p = 0
    if mask[0] == ".":
        if prev_digits > 0:
            return 0
        p = possibilities(mask[1:], pattern, 0)
    elif mask[0] == "#":
        p = possibilities(mask[1:], [pattern[0]-1,*pattern[1:]], prev_digits+1)
    elif mask[0] == "?":
        p += possibilities(mask[1:], [pattern[0]-1,*pattern[1:]], prev_digits+1)
        if prev_digits == 0:
            p += possibilities(mask[1:], pattern, 0)
    return p

# Part 1
input = read_lines("input/day12/input.txt")
sample = read_lines("input/day12/sample.txt")

value = solve_part1(sample)
assert(value == 21)
value = solve_part1(input)
assert(value == 7221)

# Part 2
#value = solve_part2(sample)
#assert(value == 525152)
#value = solve_part2(input)
#assert(value == -1)

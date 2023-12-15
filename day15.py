from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 15", "Part 1")
def solve_part1(lines: list):
    total = 0
    for instruction in lines[0].split(","):
        total += hash_alog(instruction)
    return total

@Runner("Day 15", "Part 2")
def solve_part2(lines: list):
    boxes = {}
    for instruction in lines[0].split(","):
        lens, type = parse_instruction(instruction)
        b = boxes.get(lens.lensbox, LensBox(lens.lensbox))
        boxes[b.id] = b
        if type == '=':
            b.add_lens(lens)
        else:
            b.remove_lens(lens)
    
    total = 0
    for b in boxes.values():
        total += b.focus_power()
    return total

def hash_alog(s: str) -> int:
    h = 0
    for c in s:
        h += ord(c)
        h *= 17
        h %= 256
    return h

class Lens:
    def __init__(self, label: str, length: int) -> None:
        self.label = label
        self.length = length
        self.lensbox = hash_alog(label)
        
    def __repr__(self) -> str:
        return str((self.label, self.length, self.lensbox))

class LensBox:
    def __init__(self, id: int) -> None:
        self.entries = []
        self.id = id
    
    def __repr__(self) -> str:
        return str((self.id, self.entries))
    
    def add_lens(self, lens: Lens) -> None:
        for i, l in enumerate(self.entries):
            if l.label == lens.label:
                self.entries[i] = lens
                return
        self.entries.append(lens)
    
    def remove_lens(self, lens: Lens) -> None:
        for i, l in enumerate(self.entries):
            if l.label == lens.label:
                self.entries.pop(i)
                return
    
    def focus_power(self) -> int:
        power = 0
        for i, lens in enumerate(self.entries):
            power += (self.id + 1) * (i + 1) * (lens.length)
        return power
        
def parse_instruction(s: str) -> (Lens, chr):
    for i, c in enumerate(s):
        if c == '=':
            return Lens(s[:i], int(s[i+1:])), c
        elif c == '-':
            return Lens(s[:i], 0), c

# Part 1
input = read_lines("input/day15/input.txt")
sample = read_lines("input/day15/sample.txt")

assert(hash_alog("HASH") == 52)

value = solve_part1(sample)
assert(value == 1320)
value = solve_part1(input)
assert(value == 510792)

# Part 2
value = solve_part2(sample)
assert(value == 145)
value = solve_part2(input)
assert(value == 269410)

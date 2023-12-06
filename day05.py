"""
Goal: Using a set of linked category rules, find the earliest location (last linked category)
      for a supplied set of possible seeds (first linked category).
      
Approach: Given that the seed ranges are extremely large it will not be possible to scan all
          of the provided seeds to determine the smallest location.  To combat, this code
          takes the approach of starting with the smallest ending location ranges and walking
          the category linkages up to the seed ranges that would end up mapping to those locations.
          Once that is discovered, find the first seed from the given seed ranges to intersect
          with those paths.
          
          For example when using the sample input the first location range is [0,5].  When
          mappping that back up to seeds the expand in the following ways:
          
          location: [(0, 55)]
          humidity: [(0, 55)] --> Humidity 0 results in Location of 0
          temperature: [(69, 69), (0, 54)]  --> Temperature 69 results in Humidity of 0
          light: [(65, 65), (0, 44), (77, 86)] --> Light 65 results in Temperature of 69
          water: [(72, 72), (0, 17), (25, 51), (84, 93)] --> Water of 72 results in Light of 65
          fertilizer: [(72, 72), (11, 28), (36, 52), (0, 6), (53, 55), (84, 93)]
          soil: [(72, 72), (26, 43), (51, 51), (52, 53), (0, 13), (15, 21), (14, 14), (54, 55), (84, 93)]
          seed: [(70, 70), (26, 43), (99, 99), (50, 51), (0, 13), (15, 21), (14, 14), (52, 53), (82, 91)]
"""
import sys
from utilities.data import read_lines, parse_integers
from utilities.runner import Runner

@Runner("Day 5", "Part 1")
def solve_part1(lines: list):
    a = parse_almanac(lines)
    seed_ranges = []
    for seed in a.seeds:
        seed_ranges.append((seed,seed))
    return first_location(a, seed_ranges)

@Runner("Day 5", "Part 2")
def solve_part2(lines: list):
    a = parse_almanac(lines)
    seed_ranges = []
    for i in range(int(len(a.seeds) / 2)):
        begin = a.seeds[i * 2]
        count = a.seeds[(i*2) + 1]
        seed_ranges.append((begin,begin+count-1))
    return first_location(a, seed_ranges)

class Almanac:
    def __init__(self) -> None:
        self.seeds = []
        self.catg_ranges = {}
    
    def parse_seeds(self, line: str):
        self.seeds = parse_integers(line.split(":")[1].strip(), " ")
    
    def parse_map(self, lines: list):
        c2c = lines[0].split(" ")[0].split("-")
        ranges = self.dest_target_range(c2c[0], c2c[2])
        for i in range(1, len(lines)):
            ranges.append(parse_integers(lines[i], " "))
        
    def dest_target_range(self, dest: str, target: str) -> list:
        if dest not in self.catg_ranges:
            self.catg_ranges[dest] = {}
        if target not in self.catg_ranges[dest]:
            self.catg_ranges[dest][target] = []
        return self.catg_ranges[dest][target]
    
    def dest_number(self, source: str, val: int) -> (str, int):
        c = list(self.catg_ranges[source].keys())[0]
        ranges = self.catg_ranges[source][c]
        for r in ranges:
            begin = r[1]
            end = r[1] + r[2] - 1
            if val >= begin and val <= end:
                return c, r[0] + val - r[1]
        return c, val
    
    def source_number(self, dest: str, val: int) -> (str, int):
        for k, v in self.catg_ranges.items():
            for k2, ranges in v.items():
                if k2 == dest:
                    source = k
                    for r in ranges:
                        begin = r[0]
                        end = r[0] + r[2] - 1
                        if val >= begin and val <= end:
                            return k, r[1] + val - r[0]
                    return k, val
                
    def location_ranges(self) -> list:
        for k, v in self.catg_ranges.items():
            for k2, ranges in v.items():
                if k2 == "location":
                    len_map = {}
                    start_pos = []
                    for start, _, length in ranges:
                        start_pos.append(start)
                        len_map[start] = length
                    start_pos.sort()
                    
                    loc_ranges = []
                    if start_pos[0] > 0:
                        loc_ranges.append((0, start_pos[0]-1))
                    for pos in start_pos:
                        loc_ranges.append((pos, pos + len_map[pos] - 1))
                    loc_ranges.append((start_pos[-1] + len_map[start_pos[-1]], sys.maxsize))
                    
                    return loc_ranges
    
    def ranges_to_meet(self, category: str, target_ranges: list) -> (str, list):
        for k, v in self.catg_ranges.items():
            for k2, rules in v.items():
                if k2 == category:
                    map = {}
                    start_pos = []
                    for start, target_start, length in rules:
                        start_pos.append(start)
                        map[start] = (start, start + length - 1, target_start - start)
                    start_pos.sort()
                    
                    ranges = []
                    if start_pos[0] > 0:
                        ranges.append((0, start_pos[0]-1, 0))
                    for pos in start_pos:
                        ranges.append(map[pos])
                    ranges.append((map[start_pos[-1]][1]+1, sys.maxsize, 0))
                    
                    source_ranges = []
                    for t in target_ranges:
                        b = t[0]
                        end = t[1]
                        while b <= end:
                            for r in ranges:
                                if b >= r[0] and b <= r[1]:
                                    e = end
                                    if e > r[1]:
                                        e = r[1]
                                    source_ranges.append((b+r[2], e+r[2]))
                                    b = e + 1
                                    break
                            
                    return k, source_ranges

def parse_almanac(lines: list) -> Almanac:
    a = Almanac()
    a.parse_seeds(lines[0])
    
    start, end = 2, 2
    for i in range(2, len(lines)):
        end += 1
        if lines[i] == "":
            a.parse_map(lines[start:end-1])
            start, end = i+1, i+1
    a.parse_map(lines[start:end])
    return a

def seed_location(a: Almanac, seed: int) -> int:
    c = "seed"
    val = seed
    while c != "location":
        c, val = a.dest_number(c, val)
    return val

def first_location(a: Almanac, seed_ranges: list) -> int:
    for loc_range in a.location_ranges():
        c = "location"
        r = [loc_range]
        while c != "seed":
            c, r = a.ranges_to_meet(c, r)
    
        for b, e in r:
            for seed_range in seed_ranges:
                if seed_range[0] >= b and seed_range[0] <= e:
                    return seed_location(a, seed_range[0])
                elif seed_range[0] < b and seed_range[1] > b:
                    return seed_location(a, b) 
    return -1

# Part 1
input = read_lines("input/day5-input.txt")
sample = read_lines("input/day5-sample.txt")

value = solve_part1(sample)
assert(value == 35)
value = solve_part1(input)
assert(value == 579439039)

# Part 2
value = solve_part2(sample)
assert(value == 46)
value = solve_part2(input)
assert(value == 7873084)

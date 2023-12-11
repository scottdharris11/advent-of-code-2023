import math
from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 11", "Part 1")
def solve_part1(lines: list):
    universe = Universe(lines, 2)
    return sum_distances(universe)

@Runner("Day 11", "Part 2")
def solve_part2(lines: list, empty):
    universe = Universe(lines, empty)
    return sum_distances(universe)

class Galaxy:
    def __init__(self, x, y) -> None:
        self.pos = (x, y)
        
    def __repr__(self) -> str:
        return str((self.pos))
    
class Universe:
    def __init__(self, lines, empty) -> None:
        self.empty_adjust = empty
        self.galaxies = []
        self.rows = len(lines)
        self.cols = len(lines[0])
        self.emptyrows = list(range(self.rows))
        self.emptycols = list(range(self.cols))
        
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == '#':
                    self.galaxies.append(Galaxy(x, y))
                    if y in self.emptyrows:
                        self.emptyrows.remove(y)
                    if x in self.emptycols:
                        self.emptycols.remove(x)
    
    def distance_between(self, g1: Galaxy, g2: Galaxy) -> int:
        distance = 0
        
        xrange = range(0)
        if g1.pos[0] >= g2.pos[0]:
            xrange = range(g2.pos[0], g1.pos[0])
        else:
            xrange = range(g1.pos[0], g2.pos[0])
        
        for i in xrange:
            if i in self.emptycols:
                distance += self.empty_adjust
            else:
                distance += 1
                
        yrange = range(0)
        if g1.pos[1] >= g2.pos[1]:
            yrange = range(g2.pos[1], g1.pos[1])
        else:
            yrange = range(g1.pos[1], g2.pos[1])
        
        for i in yrange:
            if i in self.emptyrows:
                distance += self.empty_adjust
            else:
                distance += 1
        
        return distance
    
def sum_distances(u: Universe) -> int:
    total = 0
    gcnt = len(u.galaxies)
    for i in range(gcnt):
        for j in range(i+1, gcnt):
            g1 = u.galaxies[i]
            g2 = u.galaxies[j]
            total += u.distance_between(g1, g2)
    return total

# Part 1
input = read_lines("input/day11-input.txt")
sample = read_lines("input/day11-sample.txt")

value = solve_part1(sample)
assert(value == 374)
value = solve_part1(input)
assert(value == 10173804)

# Part 2
value = solve_part2(sample, 10)
assert(value == 1030)
value = solve_part2(sample, 100)
assert(value == 8410)
value = solve_part2(input, 1000000)
assert(value == 634324905172)

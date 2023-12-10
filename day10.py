from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 10", "Part 1")
def solve_part1(lines: list):
    pipes = input_to_pipes(lines)

@Runner("Day 10", "Part 2")
def solve_part2(lines: list):
    return -1

VERTICAL = '|'
HORIZONTAL = "-"
NORTH_TO_EAST = "L"
NORTH_TO_WEST = "J"
SOUTH_TO_WEST = "7"
SOUTH_TO_EAST = "F"

RIGHT_FROM_CONNS = [HORIZONTAL, NORTH_TO_EAST, SOUTH_TO_EAST]
RIGHT_TO_CONNS = [HORIZONTAL, NORTH_TO_WEST, SOUTH_TO_WEST]
TOP_FROM_CONNS = [VERTICAL, NORTH_TO_EAST, NORTH_TO_WEST]
TOP_TO_CONNS = [VERTICAL, SOUTH_TO_EAST, SOUTH_TO_WEST]

START_TYPES = [
    ((True, True, False, False), HORIZONTAL),
    ((False, False, True, True), VERTICAL),
    ((True, False, True, False), NORTH_TO_WEST),
    ((True, False, False, True), SOUTH_TO_WEST),
    ((False, True, True, False), NORTH_TO_EAST),
    ((False, True, False, True), SOUTH_TO_EAST),
]

class Pipe:
    def __init__(self, x: int, y: int, type:chr) -> None:
        self.x = x
        self.y = y
        self.type = type
        self.links = []
        
    def __repr__(self):
        l = []
        for link in self.links:
            l.append((link.x, link.y))
        return str((self.x, self.y, self.type, l))
    
    def connect(self, p) -> None:
        print("Checking connection between: " + str((self.x, self.y, p.x, p.y)))
        if self.y == p.y and self.type in RIGHT_FROM_CONNS and p.type in RIGHT_TO_CONNS:
            print("connecting right: %s AND %s" % (self, p))
            self.links.append(p)
            p.links.append(self)
        elif self.x == p.x and self.type in TOP_FROM_CONNS and p.type in TOP_TO_CONNS:
            print("connecting to top: cl%s AND %s" % (self, p))
            self.links.append(p)
            p.links.append(self)
        
def input_to_pipes(lines: list[str]) -> (list[list[Pipe]], int, int):
    # parse pipes
    pipes = []
    startX, startY = 0, 0
    for y, line in enumerate(lines):
        row = []
        for x, c in enumerate(line):
            if c == "S":
                startX, startY = x, y
            if c == ".":
                row.append(None)
            else:
                row.append(Pipe(x, y, c))
        pipes.append(row)
        
    # determine starting point piece
    rowCnt = len(pipes)
    colCnt = len(pipes[0])
    possible = [False, False, False, False]
    for i, offsets in enumerate([(-1, 0), (1, 0), (0, -1), (0, 1)]):
        xo = offsets[0] + startX
        yo = offsets[1] + startY
        if xo < 0 or xo >= colCnt or yo < 0 or yo >= rowCnt:
            continue
        if pipes[yo][xo] == None:
            continue
        if xo < startX and pipes[yo][xo].type in RIGHT_FROM_CONNS:
            possible[i] = True
        if xo > startX and pipes[yo][xo].type in RIGHT_TO_CONNS:
            possible[i] = True
        if yo < startY and pipes[yo][xo].type in TOP_TO_CONNS:
            possible[i] = True
        if yo > startY and pipes[yo][xo].type in TOP_FROM_CONNS:
            possible[i] = True
    
    pt = tuple(possible)
    for s in START_TYPES:
        if s[0] == pt:
            pipes[startY][startX].type = s[1]
            break
        
    # check for connections
    for y in range(rowCnt):
        for x in range(colCnt):
            for xo, yo in [(1, 0), (0, -1)]:
                xo += x
                yo += y
                if xo >= colCnt or yo < 0:
                    continue
                if pipes[y][x] == None or pipes[yo][xo] == None:
                    continue
                pipes[y][x].connect(pipes[yo][xo])
        
    
    print(str((startX, startY)))
    for row in pipes:
        print(row)
    return pipes, startX, startY

# Part 1
input = read_lines("input/day10-input.txt")
sample = read_lines("input/day10-sample.txt")

value = solve_part1(sample)
assert(value == -1)
value = solve_part1(input)
assert(value == -1)

# Part 2
value = solve_part2(sample)
assert(value == -1)
value = solve_part2(input)
assert(value == -1)

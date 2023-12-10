from utilities.data import read_lines
from utilities.runner import Runner
from utilities.search import Search, Searcher, SearchMove

@Runner("Day 10", "Part 1")
def solve_part1(lines: list):
    pipes, start = input_to_pipes(lines)
    return int(navigate_pipe(pipes, start) / 2)

@Runner("Day 10", "Part 2")
def solve_part2(lines: list):
    pipes, _ = input_to_pipes(lines)
    outside = set()
    for y, row in enumerate(pipes):
        for x, col in enumerate(row):
            if col == None:
                pos = (x, y)
                if pos not in outside:
                    es = EdgeSearcher(pos, pipes, outside)
                    s = Search(es)
                    solution = s.best(SearchMove(0, pos))
                    if solution == None:
                        continue
                    outside = outside.union(solution.path)

    inside = 0
    for y, row in enumerate(pipes):
        for x, col in enumerate(row):
            if col == None:
                pos = (x, y)
                if pos not in outside:
                    inside += 1
    return inside

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

POSSIBLE_TYPES = [
    ((True, True, False, False), HORIZONTAL),
    ((False, False, True, True), VERTICAL),
    ((True, False, True, False), NORTH_TO_WEST),
    ((True, False, False, True), SOUTH_TO_WEST),
    ((False, True, True, False), NORTH_TO_EAST),
    ((False, True, False, True), SOUTH_TO_EAST),
]

class Pipe:
    def __init__(self, x: int, y: int, type:chr) -> None:
        self.pos = (x, y)
        self.type = type
        self.links = []
        self.inloop = False
        
    def __repr__(self):
        return str((self.pos, self.type, self.links))
    
    def connect(self, p) -> None:
        if self.pos[1] == p.pos[1] and self.type in RIGHT_FROM_CONNS and p.type in RIGHT_TO_CONNS:
            self.links.append(p.pos)
            p.links.append(self.pos)
        elif self.pos[0] == p.pos[0] and self.type in TOP_FROM_CONNS and p.type in TOP_TO_CONNS:
            self.links.append(p.pos)
            p.links.append(self.pos)

class EdgeSearcher(Searcher):
    def __init__(self, point: tuple[int], pipes: list[list[Pipe]], outside: list[tuple]) -> None:
        self.point = point
        self.pipes = pipes
        self.rows = len(pipes)
        self.cols = len(pipes[0])
        self.outside = outside
        
    def is_goal(self, obj) -> bool:
        if obj in self.outside:
            return True
        if obj[0] <= 0 or obj[0] >= self.cols:
            return True
        if obj[1] <= 0 or obj[1] >= self.rows:
            return True
        return False
    
    def possible_moves(self, obj) -> list[SearchMove]:
        moves = []
        for xo, yo in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            xo += obj[0]
            yo += obj[1]
            if xo < 0 or xo >= self.cols or yo < 0 or yo >= self.rows:
                continue
            if self.pipes[yo][xo] == None:
                moves.append(SearchMove(1, (xo, yo)))
        return moves
    
    def distance_from_goal(self, obj) -> int:
        return min(obj[0], obj[1])
    
def input_to_pipes(lines: list[str]) -> (list[list[Pipe]], tuple):
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
    for s in POSSIBLE_TYPES:
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
        
    return pipes, (startX, startY)

def navigate_pipe(pipes: list[list[Pipe]], start: tuple[int]) -> int:
    steps = 0
    prev = start
    loc = pipes[start[1]][start[0]].links[0]
    while True:
        steps += 1
        pipe = pipes[loc[1]][loc[0]]
        pipe.inloop = True
        
        if start == pipe.pos:
            break
        
        for link in pipe.links:
            if link == prev:
                continue
            prev = loc
            loc = link
            break
    return steps

# Part 1
input = read_lines("input/day10-input.txt")
sample = read_lines("input/day10-sample.txt")
sample2 = read_lines("input/day10-sample2.txt")
sample3 = read_lines("input/day10-sample3.txt")
sample4 = read_lines("input/day10-sample4.txt")

value = solve_part1(sample)
assert(value == 4)
value = solve_part1(sample2)
assert(value == 8)
value = solve_part1(input)
assert(value == 6738)

# Part 2
value = solve_part2(sample3)
assert(value == 4)
value = solve_part2(sample4)
assert(value == 4)
value = solve_part2(input)
assert(value == -1)

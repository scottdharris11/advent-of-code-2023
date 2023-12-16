from utilities.data import read_lines
from utilities.runner import Runner
from utilities.search import Search, Searcher, SearchMove

@Runner("Day 10", "Part 1")
def solve_part1(lines: list):
    pipes, start = input_to_pipes(lines)
    return int(navigate_pipe(pipes, start) / 2)

@Runner("Day 10", "Part 2")
def solve_part2(lines: list):
    pipes, start = input_to_pipes(lines)
    navigate_pipe(pipes, start)
    maze = PipeMaze(pipes)
    inside = set()
    for y in range(maze.row_count):
        for x in range(maze.col_count):
            pos = (x, y)
            if maze.inside(pos):
                inside.add(pos)
    return len(inside)

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
        return str((self.pos, self.type, self.links, self.inloop))
    
    def connect(self, p) -> None:
        if self.pos[1] == p.pos[1] and self.type in RIGHT_FROM_CONNS and p.type in RIGHT_TO_CONNS:
            self.links.append(p.pos)
            p.links.append(self.pos)
        elif self.pos[0] == p.pos[0] and self.type in TOP_FROM_CONNS and p.type in TOP_TO_CONNS:
            self.links.append(p.pos)
            p.links.append(self.pos)

class PipeMaze:
    def __init__(self, pipes: list[list[Pipe]]) -> None:
        self.pipes = pipes
        self.row_count = len(pipes)
        self.col_count = len(pipes[0])
    
    def inside(self, point: tuple[int]) -> bool:
        if self.__pipe(point[0], point[1]) != None:
            return False
        bottom = self.vert_pipes_to_outside(point, 1)
        top = self.vert_pipes_to_outside(point, -1)
        right = self.horz_pipes_to_outside(point, 1)
        left = self.horz_pipes_to_outside(point, -1)
        if bottom == 0 or top == 0 or right == 0 or left == 0:
            return False
        if bottom % 2 == 0 or top % 2 == 0 or right % 2 == 0 or left % 2 == 0:
            return False
        return True
    
    def vert_pipes_to_outside(self, point: tuple[int], dir: int) -> int:
        crossed = 0
        y = point[1] + dir
        elbow = ""
        while y >= 0 and y < self.row_count:
            p = self.__pipe(point[0], y)
            y += dir
            if p == None or p.type == VERTICAL:
                continue
            crossed += 1
            if p.type == HORIZONTAL:
                continue
            if p.type == NORTH_TO_EAST and elbow == SOUTH_TO_EAST:
                crossed -= 2
                elbow = ""
            elif p.type == SOUTH_TO_EAST and elbow == NORTH_TO_EAST:
                crossed -= 2
                elbow = ""
            elif p.type == NORTH_TO_EAST and elbow == SOUTH_TO_WEST:
                crossed -= 1
                elbow = ""
            elif p.type == SOUTH_TO_EAST and elbow == NORTH_TO_WEST:
                crossed -= 1
                elbow = ""
            elif p.type == NORTH_TO_WEST and elbow == SOUTH_TO_WEST:
                crossed -= 2
                elbow = ""
            elif p.type == SOUTH_TO_WEST and elbow == NORTH_TO_WEST:
                crossed -= 2
                elbow = ""
            elif p.type == NORTH_TO_WEST and elbow == SOUTH_TO_EAST:
                crossed -= 1
                elbow = ""
            elif p.type == SOUTH_TO_WEST and elbow == NORTH_TO_EAST:
                crossed -= 1
                elbow = ""
            else:
                elbow = p.type
        return crossed
    
    def horz_pipes_to_outside(self, point: tuple[int], dir: int) -> int:
        crossed = 0
        x = point[0] + dir
        elbow = ""
        while x >= 0 and x < self.col_count:
            p = self.__pipe(x, point[1])
            x += dir
            if p == None or p.type == HORIZONTAL:
                continue
            crossed += 1
            if p.type == VERTICAL:
                continue
            if p.type == NORTH_TO_EAST and elbow == NORTH_TO_WEST:
                crossed -= 2
                elbow = ""
            elif p.type == SOUTH_TO_EAST and elbow == SOUTH_TO_WEST:
                crossed -= 2
                elbow = ""
            elif p.type == NORTH_TO_EAST and elbow == SOUTH_TO_WEST:
                crossed -= 1
                elbow = ""
            elif p.type == SOUTH_TO_EAST and elbow == NORTH_TO_WEST:
                crossed -= 1
                elbow = ""
            elif p.type == NORTH_TO_WEST and elbow == NORTH_TO_EAST:
                crossed -= 2
                elbow = ""
            elif p.type == SOUTH_TO_WEST and elbow == SOUTH_TO_EAST:
                crossed -= 2
                elbow = ""
            elif p.type == NORTH_TO_WEST and elbow == SOUTH_TO_EAST:
                crossed -= 1
                elbow = ""
            elif p.type == SOUTH_TO_WEST and elbow == NORTH_TO_EAST:
                crossed -= 1
                elbow = ""
            else:
                elbow = p.type
        return crossed
        
    def __pipe(self, x: int, y: int) -> Pipe:
        if x < 0 or x >= self.col_count or y < 0 or y >= self.row_count:
            return None
        pipe = self.pipes[y][x]
        if pipe == None:
            return None
        if not pipe.inloop:
            return None
        return pipe

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
input = read_lines("input/day10/input.txt")
sample = read_lines("input/day10/sample.txt")
sample2 = read_lines("input/day10/sample2.txt")
sample3 = read_lines("input/day10/sample3.txt")
sample4 = read_lines("input/day10/sample4.txt")
sample5 = read_lines("input/day10/sample5.txt")
sample6 = read_lines("input/day10/sample6.txt")

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
value = solve_part2(sample5)
assert(value == 8)
value = solve_part2(sample6)
assert(value == 10)
value = solve_part2(input)
assert(value == 579)

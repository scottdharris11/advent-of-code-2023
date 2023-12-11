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
    outside = set()
    for y, row in enumerate(pipes):
        for x, col in enumerate(row):
            if col == None or not col.inloop:
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
            if col == None or not col.inloop:
                pos = (x, y)
                if pos not in outside:
                    print(pos)
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
        return str((self.pos, self.type, self.links, self.inloop))
    
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
        if obj[0] < 0 or obj[0] == self.cols:
            return True
        if obj[1] < 0 or obj[1] == self.rows:
            return True
        return False
    
    def __pipe(self, x: int, y: int) -> Pipe:
        if x < 0 or x >= self.cols or y < 0 or y >= self.rows:
            return None
        pipe = self.pipes[y][x]
        if pipe == None:
            return None
        if not pipe.inloop:
            return None
        return pipe
    
    def possible_moves(self, obj) -> list[SearchMove]:
        moves = set()
        x, y = obj
        for xo, yo in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            xo += x
            yo += y
            if xo == -1 or xo == self.cols or yo == -1 or yo == self.rows:
                moves.add((xo, yo))
            elif self.pipes[yo][xo] == None or not self.pipes[yo][xo].inloop:
                moves.add((xo, yo))
        
        for left, right, yo, dir in [(x-1, x, -1, 'U'), (x, x+1, -1, 'U'), (x-1, x, 1, 'D'), (x, x+1, 1, 'D')]:
            v = y + yo
            lpipe = self.__pipe(left, v)
            rpipe = self.__pipe(right, v)
            
            if lpipe == None or rpipe == None:
                if lpipe == None:
                    moves.add((left, v))
                if rpipe == None:
                    moves.add((right, v))
            else:
                if lpipe.pos not in rpipe.links:
                    self.__squeeze(lpipe.pos, rpipe.pos, moves, dir, set())
        
        for top, bottom, xo, dir in [(y-1, y, -1, 'L'), (y, y+1, -1, 'L'), (y-1, y, 1, 'R'), (y, y+1, 1, 'R')]:
            h = x + xo
            tpipe = self.__pipe(h, top)
            bpipe = self.__pipe(h, bottom)
            
            if tpipe == None or bpipe == None:
                if tpipe == None:
                    moves.add((h, top))
                if bpipe == None:
                    moves.add((h, bottom))
            else:
                if tpipe.pos not in bpipe.links:
                    self.__squeeze(tpipe.pos, bpipe.pos, moves, dir, set())
                
        rmoves = []
        for move in moves:
            rmoves.append(SearchMove(1, move))
        return rmoves
    
    def distance_from_goal(self, obj) -> int:
        fromleft = obj[0]
        fromright = self.cols - obj[0]
        fromtop = obj[1]
        frombottom = self.rows - obj[1]
        m = min(fromleft, fromright, fromtop, frombottom)
        if m < 0:
            return 0
        else:
            return m + 1
            
    def __squeeze(self, pos1, pos2, moves, dir, searched):    
        pos1x, pos1y = pos1
        pos2x, pos2y = pos2
        s = (pos1x, pos1y, pos2x, pos2y)
        if s in searched:
            return
        searched.add(s)
        
        checks = []
        if dir == 'L':
            checks = [
                ('L', pos1x-1, pos1y, pos2x-1, pos2y), 
                ('D', pos2x-1, pos2y, pos2x, pos2y),
                ('U', pos1x-1, pos1y, pos1x, pos1y), 
            ]
        elif dir == 'R':
            checks = [
                ('R', pos1x+1, pos1y, pos2x+1, pos2y), 
                ('D', pos2x, pos2y, pos2x+1, pos2y),
                ('U', pos1x, pos1y, pos1x+1, pos1y),
            ]
        elif dir == 'D':
            checks = [
                ('D', pos1x, pos1y+1, pos2x, pos2y+1), 
                ('R', pos2x, pos2y, pos2x, pos2y+1), 
                ('L', pos1x, pos1y, pos1x, pos1y+1),
            ]
        else:
            checks = [
                ('U', pos1x, pos1y-1, pos2x, pos2y-1), 
                ('R', pos2x, pos2y+1, pos2x, pos2y), 
                ('L', pos1x, pos1y+1, pos1x, pos1y),
            ]
        
        for check in checks:
            pos1pipe = self.__pipe(check[1], check[2])
            pos2pipe = self.__pipe(check[3], check[4])
            
            if pos1pipe == None or pos2pipe == None:
                if pos1pipe == None:
                    moves.add((check[1], check[2]))
                if pos2pipe == None:
                    moves.add((check[3], check[4]))
            else:
                if pos1pipe.pos not in pos2pipe.links:
                    self.__squeeze(pos1pipe.pos, pos2pipe.pos, moves, check[0], searched)
    
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
sample5 = read_lines("input/day10-sample5.txt")
sample6 = read_lines("input/day10-sample6.txt")

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
assert(value < 809)
assert(value != 686)
assert(value == -1)

import cProfile
from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 21", "Part 1")
def solve_part1(lines: list, steps: int):
    m = Map(lines)
    for _ in range(steps):
        m.step()
    return m.possible_locations()

@Runner("Day 21", "Part 2")
def solve_part2(lines: list, steps: int):
    m = Map(lines)
    for _ in range(steps):
        m.step()
    return m.possible_locations()

class Map:
    def __init__(self, lines: list) -> None:
        self.grid = lines
        self.row_count = len(lines)
        self.col_count = len(lines[0])
        self.move_cache = {}
        self.tiles = {}
        self.max = 0
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if col == "S":
                    self.tiles[(0,0)] = MapTile((0,0), (x, y))
                if col != "#":
                    self.max += 1
    
    def step(self) -> None:
        lasttilekey = None
        lasttile = None
        for key, tile in self.tiles.copy().items():
            if tile.maxed:
                continue
            for location in tile.locations():
                if location not in self.move_cache:
                    self.move_cache[location] = self.moves(location)
                moves = self.move_cache[location]
                for move in moves:
                    tilekey = (key[0]+move[2], key[1]+move[3])
                    if lasttile == None or lasttilekey != tilekey:
                        if tilekey not in self.tiles:
                            self.tiles[tilekey] = MapTile(tilekey, None)
                        lasttile = self.tiles[tilekey]
                        lasttilekey = tilekey
                    lasttile.add_step((move[0], move[1]))
        for tile in self.tiles.values():
            tile.complete_cycle(self.max)
    
    def moves(self, location: tuple[int]) -> list[tuple[int]]:
        moves = []
        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            tx = 0
            ty = 0
            nx = location[0] + move[0]
            ny = location[1] + move[1]
            
            if nx < 0:
                nx = self.col_count - 1
                tx = -1
            elif nx == self.col_count:
                nx = 0
                tx = 1
            elif ny < 0:
                ny = self.row_count - 1
                ty = -1
            elif ny == self.row_count:
                ny = 0
                ty = 1
                
            if self.grid[ny][nx] == "#":
                continue
            
            moves.append((nx, ny, tx, ty))
        return moves
    
    def possible_locations(self) -> int:
        total = 0
        for tile in self.tiles.values():
            total += tile.plots_reachable()
        return total

class MapTile:
    def __init__(self, sliver: tuple[int], start: tuple[int]) -> None:
        self.sliver = sliver
        self.plots = set()
        if start != None:
            self.plots.add(start)
        self.stage = set()
        self.maxed = False
        self.prev = 0
        self.last = 0
        self.maxcnt = 0
        
    def add_step(self, step: tuple[int]) -> None:
        if self.maxed:
            return
        self.stage.add(step)
        
    def complete_cycle(self, max: int) -> None:
        if self.maxed:
            t = self.prev
            self.prev = self.last
            self.last = t
            return
        
        self.prev = self.last
        self.last = len(self.stage)
        if self.last > max/2:
            self.maxcnt += 1
        if self.maxcnt >= 10:
            self.maxed = True
            self.plots = None
            self.stage = None
        else:
            self.plots = self.stage
            self.stage = set()
        
    def locations(self) -> set[tuple[int]]:
        if self.maxed:
            return []
        return self.plots
    
    def plots_reachable(self) -> int:
        return self.last

# Part 1
input = read_lines("input/day21/input.txt")
sample = read_lines("input/day21/sample.txt")

value = solve_part1(sample, 6)
assert(value == 16)
value = solve_part1(input, 64)
assert(value == 3820)

# Part 2
value = solve_part2(sample, 6)
assert(value == 16)
value = solve_part2(sample, 10)
assert(value == 50)
value = solve_part2(sample, 50)
assert(value == 1594)
value = solve_part2(sample, 100)
assert(value == 6536)
value = solve_part2(sample, 500)
assert(value == 167004)
value = solve_part2(sample, 1000)
assert(value == 668697)
value = solve_part2(sample, 5000)
assert(value == 16733044)
#value = solve_part2(input, 26501365)
#assert(value == -1)

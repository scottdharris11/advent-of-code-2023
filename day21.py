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
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if col == "S":
                    self.tiles[(0,0)] = set()
                    self.tiles[(0,0)].add((x, y))
                    return
    
    def step(self) -> None:
        ntiles = {}
        lasttilekey = None
        lasttile = None
        for tile in self.tiles.keys():
            for location in self.tiles[tile]:
                if location not in self.move_cache:
                    self.move_cache[location] = self.moves(location)
                moves = self.move_cache[location]
                for move in moves:
                    tilekey = (tile[0]+move[2], tile[1]+move[3])
                    if lasttile == None or lasttilekey != tilekey:
                        lasttile = ntiles.get(tilekey, set())
                        lasttilekey = tilekey
                    lasttile.add((move[0], move[1]))
                    ntiles[tilekey] = lasttile
        self.tiles = ntiles
    
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
            total += len(tile)
        return total

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
#value = solve_part2(sample, 1000)
#assert(value == 668697)
#value = solve_part2(sample, 5000)
#assert(value == 16733044)
#value = solve_part2(input, 26501365)
#assert(value == -1)

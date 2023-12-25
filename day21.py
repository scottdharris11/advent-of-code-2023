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
        self.states = {}
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if col == "S":
                    state = MapTileState()
                    state.plots.add((x, y))
                    state.active = 1
                    self.states[hash(state)] = state
                    return
    
    def step(self) -> None:
        for state in self.states.copy().values():
            if state.active == 0:
                continue
            if state.next == None:
                state.next = self.next_states(state)
            for n in state.next:
                self.states[n].stage(state.active)
        for state in self.states.values():
            state.commit()
    
    def next_states(self, state: "MapTileState") -> list["MapTileState"]:
        tiles = {}
        for location in state.plots:
            if location not in self.move_cache:
                self.move_cache[location] = self.moves(location)
            moves = self.move_cache[location]
            for move in moves:
                xy = (move[0], move[1])
                key = (move[2], move[3])
                if key not in tiles:
                    tiles[key] = MapTileState()
                tiles[key].plots.add(xy)
        
        states = []
        for tile in tiles.values():
            h = hash(tile)
            if h not in self.states:
                tile.locations = len(tile.plots)
                self.states[h] = tile
            states.append(h)
        return states

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
        for state in self.states.values():
            total += state.active * state.locations
        return total

class MapTileState:
    def __init__(self) -> None:
        self.plots = set()
        self.locations = 0
        self.next = None
        self.active = 0
        self.staged = 0
        
    def __hash__(self) -> int:
        h = 0
        for plot in self.plots:
            h += hash(plot)
        return h

    def stage(self, count: int) -> None:
        self.staged += count
    
    def commit(self) -> None:
        self.active = self.staged
        self.staged = 0

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

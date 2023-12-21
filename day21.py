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
        self.locations = [[0 for _ in range(self.col_count)] for _ in range(self.row_count)]
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if col == "S":
                    self.locations[y][x] = 1
                    return
    
    def step(self) -> None:
        nlocs = [[0 for _ in range(self.col_count)] for _ in range(self.row_count)]
        for y, row in enumerate(self.locations):
            for x, col in enumerate(row):
                if col == 0:
                    continue
                for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx = x + move[0]
                    ny = y + move[1]
                    
                    if nx < 0:
                        nx = self.col_count - 1
                        if self.locations[y][nx] > 0:
                            continue
                    elif nx == self.col_count:
                        nx = 0
                        if self.locations[y][nx] > 0:
                            continue
                    elif ny < 0:
                        ny = self.row_count - 1
                        if self.locations[ny][x] > 0:
                            continue
                    elif ny == self.row_count:
                        ny = 0
                        if self.locations[ny][x] > 0:
                            continue
                    
                    if self.grid[ny][nx] == "#":
                        continue
                    nlocs[ny][nx] = 1 * col
        self.locations = nlocs
        
    def possible_locations(self) -> int:
        total = 0
        for row in self.locations:
            for col in row:
                total += col
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
value = solve_part2(sample, 1000)
assert(value == 668697)
value = solve_part2(sample, 5000)
assert(value == 16733044)
value = solve_part2(input, 26501365)
assert(value == -1)

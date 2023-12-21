from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 21", "Part 1")
def solve_part1(lines: list, steps: int):
    m = Map(lines)
    before = [m.start]
    for _ in range(steps):
        after = set()
        for b in before:
            after.update(m.moves_from(b))
        before.clear()
        before.extend(after)
    return len(before)

@Runner("Day 21", "Part 2")
def solve_part2(lines: list, steps: int):
    m = Map(lines)
    before = [m.start]
    for _ in range(steps):
        after = set()
        for b in before:
            after.update(m.moves_from(b))
        before.clear()
        before.extend(after)
    return len(before)

class Map:
    def __init__(self, lines: list) -> None:
        self.grid = lines
        self.row_count = len(lines)
        self.col_count = len(lines[0])
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if col == "S":
                    self.start = (x, y, 0, 0)
                    return
    
    def moves_from(self, current: tuple[int]) -> list[tuple[int]]:
        moves = []
        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx = current[0] + move[0]
            ny = current[1] + move[1]
            mx = current[2]
            my = current[3]
            
            if nx < 0:
                mx -= 1
                nx = self.col_count - 1
            elif nx == self.col_count:
                mx += 1
                nx = 0
            if ny < 0:
                my -= 1
                ny = self.row_count - 1
            elif ny == self.row_count:
                my += 1
                ny = 0
            
            if self.grid[ny][nx] == "#":
                continue
            moves.append((nx, ny, mx, my))
        return moves

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

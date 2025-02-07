"""utility imports"""
import functools
from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 21", "Part 1")
def solve_part1(lines: list, steps: int):
    """Solution for part 1"""
    return reachable_plots(Farm(lines), steps)

@Runner("Day 21", "Part 2")
def solve_part2(lines: list, steps: int):
    """Solution for part 2"""
    return reachable_plots(Farm(lines), steps)

class Farm:
    """Farm map"""
    def __init__(self, lines: list) -> None:
        self.rocks = set()
        self.height = len(lines)
        self.width = len(lines[0])
        for y, row in enumerate(lines):
            for x, col in enumerate(row):
                if col == "S":
                    self.start = (x, y)
                if col == "#":
                    self.rocks.add((x,y))

    @functools.lru_cache(maxsize=5000)
    def moves_from(self, current: tuple[int]) -> list[tuple[int]]:
        """possible moves in one step from a location"""
        x = current[0]
        if x < 0 or x >= self.width:
            x %= self.width
        y = current[1]
        if y < 0 or y >= self.height:
            y %= self.height
        moves = []
        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx = current[0] + move[0]
            ny = current[1] + move[1]
            if (x + move[0], y + move[1]) in self.rocks:
                continue
            moves.append((nx, ny))
        return moves

def reachable_plots(farm: Farm, steps: int) -> int:
    """determine the plots reachable in a number of steps"""
    before = set()
    before.add(farm.start)
    for _ in range(steps):
        after = set()
        for b in before:
            after.update(farm.moves_from(b))
        before = after
        #print("step " + str(i+1) + ": " + str(len(before)))
        #print(before)
    return len(before)

# Data
data = read_lines("input/day21/input.txt")
sample = read_lines("input/day21/sample.txt")

# Part 1
assert solve_part1(sample, 6) == 16
assert solve_part1(data, 64) == 3820

# Part 2
assert solve_part2(sample, 6) == 16
assert solve_part2(sample, 10) == 50
assert solve_part2(sample, 50) == 1594
assert solve_part2(sample, 100) == 6536
#assert solve_part2(sample, 500) == 167004
#assert solve_part2(data) == -1

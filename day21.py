"""utility imports"""
import functools
from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 21", "Part 1")
def solve_part1(lines: list, steps: int):
    """Solution for part 1"""
    return reachable_plots(Farm(lines), steps)[steps]

@Runner("Day 21", "Part 2")
def solve_part2(lines: list, steps: int):
    """Solution for part 2"""
    farm = Farm(lines)
    half = len(lines) // 2
    full = len(lines)
    reachable = reachable_plots(farm, (full * 3)+half)
    times = (steps - half) // full
    sequence = []
    sequence.append(reachable[half])
    sequence.append(reachable[full + half])
    sequence.append(reachable[(full * 2) + half])
    sequence.append(reachable[(full * 3) + half])
    while len(sequence) <= times:
        sequence.append(next_value(sequence[-4:]))
    return sequence[-1]

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

def reachable_plots(farm: Farm, steps: int) -> dict:
    """determine the plots reachable in a number of steps"""
    reached = {}
    q = []
    visited = set()
    q.append((0,farm.start))
    visited.add(farm.start)
    while len(q) > 0:
        s, pos = q.pop(0)
        if s > steps:
            continue
        if s not in reached and s >= 2:
            reached[s] = reached.get(s-2)
        reached[s] = reached.get(s,0)+1
        moves = farm.moves_from(pos)
        for move in moves:
            if move not in visited:
                q.append((s+1, move))
                visited.add(move)
    return reached

def next_value(values: list[int]) -> int:
    """for a given sequence of values, determine the next value (from day 9, quadratic sequence)"""
    diffs = []
    allzeroes = True
    for i in range(len(values)-1):
        d = values[i+1] - values[i]
        diffs.append(d)
        if values[i+1] != 0 or values[i] != 0:
            allzeroes = False
    if allzeroes:
        return 0
    return values[-1] + next_value(diffs)

# Data
data = read_lines("input/day21/input.txt")
sample = read_lines("input/day21/sample.txt")

# Part 1
assert solve_part1(sample, 6) == 16
assert solve_part1(data, 64) == 3820

# Part 2
assert solve_part2(data, 26501365) == 632421652138917

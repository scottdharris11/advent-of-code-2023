"""utility imports"""
from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 21", "Part 1")
def solve_part1(lines: list, steps: int):
    """Solution for part 1"""
    return reachable_plots(Farm(lines), steps)[steps]

@Runner("Day 21", "Part 2")
def solve_part2(lines: list, steps: int):
    """Solution for part 2"""
    # Needed a great deal of help with this part. Several hints in the aoc reddit thread lead me
    # to understand the extrapolation necessary (not possible to actually compute that many steps).
    # understanding that the work done on day 9 set the stage for calculating the next value was a
    # key step however still needed additional help to unlock.  The fact that the step amount was
    # dividable (to the tune of 202300 when taking the grid width (131) plus half the grid
    # width (65)) is something i would not have come to on my own.  Also the fact that in the real
    # inputs there would end up being a clear path from starting position to the extremes (walking
    # straight up, down, left, right) which was different than the sample.  I ended up using the
    # sample only to ensure I was calculating the offsets properly back to the original grid for
    # comparison purposes.  After that, the below method didn't work for it since the rocks didn't
    # lend it to a uniform method. The next problem that I had was understanding how many I had to
    # calculate before starting the projections.  Even after using the site:
    # https://www.dcode.fr/lagrange-interpolating-polynomial?__r=1.3f4afcaf435bf67e6bd25ca5495fbd5b
    # to do a "langrange interpoloating ploynomial" calculation, had to realize that I needed to
    # start with 4 values to project the next value correctly.  This blog post was helpful to me
    # in understanding the solution:
    # https://www.ericburden.work/blog/2023/12/21/advent-of-code-day-21/
    #
    # Value 1: Half a grid (65 steps)
    # Value 2: Full grid plus half (131 + 65 = 196)
    # Value 3: 2x full grid plus half (262 + 65 = 327)
    # Value 4: 3x full grid plus half (393 + 65 = 458)
    #
    # From there it was just a matter of projecting the next value enough times to arrive at
    # the desired step amount.
    farm = Farm(lines)
    half = len(lines) // 2
    full = len(lines)
    reachable = reachable_plots(farm, (full * 3)+half)
    sequence = [reachable[half], reachable[full + half], 
                reachable[(full * 2) + half], reachable[(full * 3) + half]]
    s = (full * 3) + half
    while s < steps:
        sequence.append(next_value(sequence[-4:]))
        s += full
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
    # adjusted this for a bit better performance on higher step
    # counts to use a queue approach to not recalculate steps
    # again. trick was to know that odd and even steps roll into
    # one another.  using a dictionary to avoid redoing calculations
    # for several different step points.
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

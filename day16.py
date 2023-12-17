from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 16", "Part 1")
def solve_part1(lines: list):
    return energize_tiles(lines, Beam(-1, 0, RIGHT))

@Runner("Day 16", "Part 2")
def solve_part2(lines: list):
    row_count = len(lines)
    col_count = len(lines[0])
    value = 0
    for y in range(row_count):
        for x in range(col_count):
            if x == 0:
                value = max(value, energize_tiles(lines, Beam(x-1, y, RIGHT)))
                value = max(value, energize_tiles(lines, Beam(col_count, y, LEFT)))
            if y == 0:
                value = max(value, energize_tiles(lines, Beam(x, y-1, DOWN)))
                value = max(value, energize_tiles(lines, Beam(x, row_count, UP)))
    return value

RIGHT = "R"
LEFT = "L"
UP = "U"
DOWN = "D"

MOVES = {
    '.': {RIGHT: [RIGHT], LEFT: [LEFT], UP: [UP], DOWN: [DOWN]},
    '/': {RIGHT: [UP], LEFT: [DOWN], UP: [RIGHT], DOWN: [LEFT]},
    '\\': {RIGHT: [DOWN], LEFT: [UP], UP: [LEFT], DOWN: [RIGHT]},
    '|': {RIGHT: [DOWN, UP], LEFT: [DOWN, UP], UP: [UP], DOWN: [DOWN]},
    '-': {RIGHT: [RIGHT], LEFT: [LEFT], UP: [RIGHT, LEFT], DOWN: [RIGHT, LEFT]}
}

class Beam:
    def __init__(self, x: int, y: int, dir: str) -> None:
        self.x = x
        self.y = y
        self.moving = dir
        
    def __repr__(self) -> str:
        return str((self.x, self.y, self.moving))

def energize_tiles(lines: list, start: Beam) -> int:
    c = Contraption(lines, start)
    while c.energize():
        pass
    return len(c.energized)
    
class Contraption:
    def __init__(self, grid: list[str], initbeam: Beam) -> None:
        self.grid = grid
        self.row_count = len(grid)
        self.col_count = len(grid[0])
        self.beams = [initbeam]
        self.energized = set()
        self.energy_direction = set()
    
    def __repr__(self) -> str:
        sb = "\n"
        for y, row in enumerate(self.grid):
            for x, _ in enumerate(row):
                pos = (x, y)
                if pos in self.energized:
                    sb += "#"
                else:
                    sb += "."
            sb += "\n"
        sb += "\n"
        return sb
    
    def energize(self) -> bool:
        energy_before = len(self.energy_direction)
        prune_idxs = []
        for i in range(len(self.beams)):
            beam = self.beams[i]
            prune = False
            if beam.moving == RIGHT:
                prune = self.__move_beam(beam, 1, 0)
            elif beam.moving == LEFT:
                prune = self.__move_beam(beam, -1, 0)
            elif beam.moving == UP:
                prune = self.__move_beam(beam, 0, -1)
            elif beam.moving == DOWN:
                prune = self.__move_beam(beam, 0, 1)
            if prune:
                prune_idxs.append(i)
        for i in range(len(prune_idxs)-1, -1, -1):
            self.beams.pop(prune_idxs[i])
        return len(self.energy_direction) != energy_before
    
    def __move_beam(self, b: Beam, xOffset: int, yOffset: int) -> bool:
        if ( b.x + xOffset < 0 or
            b.x + xOffset == self.col_count or 
            b.y + yOffset < 0 or
            b.y + yOffset == self.row_count ):
            return True
        b.x += xOffset
        b.y += yOffset
        
        locdir = (b.x, b.y, b.moving)
        if locdir in self.energy_direction:
            return True
        self.energized.add((b.x, b.y))
        self.energy_direction.add(locdir)
        
        type = self.grid[b.y][b.x]
        directions = MOVES[type][b.moving]
        b.moving = directions[0]
        for i in range(1, len(directions)):
            self.beams.append(Beam(b.x, b.y, directions[i]))

# Part 1
input = read_lines("input/day16/input.txt")
sample = read_lines("input/day16/sample.txt")

value = solve_part1(sample)
assert(value == 46)
value = solve_part1(input)
assert(value == 8146)

# Part 2
value = solve_part2(sample)
assert(value == 51)
value = solve_part2(input)
assert(value == 8358)

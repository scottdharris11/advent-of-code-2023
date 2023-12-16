from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 16", "Part 1")
def solve_part1(lines: list):
    c = Contraption(lines)
    while c.energize():
        pass
    return len(c.energized)

@Runner("Day 16", "Part 2")
def solve_part2(lines: list):
    return -1

RIGHT = "R"
LEFT = "L"
UP = "U"
DOWN = "D"
STOPPED = "S"

class Beam:
    def __init__(self, x: int, y: int, dir: str) -> None:
        self.x = x
        self.y = y
        self.moving = dir
        
    def __repr__(self) -> str:
        return str((self.x, self.y, self.moving))
    
class Contraption:
    def __init__(self, grid: list[str]) -> None:
        self.grid = grid
        self.row_count = len(grid)
        self.col_count = len(grid[0])
        self.beams = [Beam(-1, 0, RIGHT)]
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
        stopped_idxs = []
        for i in range(len(self.beams)):
            beam = self.beams[i]
            stopped = False
            if beam.moving == RIGHT:
                stopped = self.__move_beam_right(beam)
            elif beam.moving == LEFT:
                stopped = self.__move_beam_left(beam)
            elif beam.moving == UP:
                stopped = self.__move_beam_up(beam)
            elif beam.moving == DOWN:
                stopped = self.__move_beam_down(beam)
            if stopped:
                stopped_idxs.append(i)
        for i in range(len(stopped_idxs)-1, -1, -1):
            self.beams.pop(stopped_idxs[i])
        return len(self.energy_direction) != energy_before
    
    def __move_beam_right(self, b: Beam) -> bool:
        if b.x + 1 == self.col_count:
            b.moving = STOPPED
            return True
        b.x += 1
        self.energized.add((b.x, b.y))
        self.energy_direction.add((b.x, b.y, b.moving))
        type = self.grid[b.y][b.x]
        if type == '/':
            b.moving = UP
        elif type == '\\':
            b.moving = DOWN
        elif type == "|":
            b.moving = DOWN
            self.beams.append(Beam(b.x, b.y, UP))
        return False
        
    def __move_beam_left(self, b: Beam) -> bool:
        if b.x - 1 < 0:
            b.moving = STOPPED
            return True
        b.x -= 1
        self.energized.add((b.x, b.y))
        self.energy_direction.add((b.x, b.y, b.moving))
        type = self.grid[b.y][b.x]
        if type == '/':
            b.moving = DOWN
        elif type == '\\':
            b.moving = UP
        elif type == "|":
            b.moving = DOWN
            self.beams.append(Beam(b.x, b.y, UP))
        return False

    def __move_beam_up(self, b: Beam) -> bool:
        if b.y - 1 < 0:
            b.moving = STOPPED
            return True
        b.y -= 1
        self.energized.add((b.x, b.y))
        self.energy_direction.add((b.x, b.y, b.moving))
        type = self.grid[b.y][b.x]
        if type == '/':
            b.moving = RIGHT
        elif type == '\\':
            b.moving = LEFT
        elif type == "-":
            b.moving = RIGHT
            self.beams.append(Beam(b.x, b.y, LEFT))
        return False
    
    def __move_beam_down(self, b: Beam) -> bool:
        if b.y + 1 == self.row_count:
            b.moving = STOPPED
            return True
        b.y += 1
        self.energized.add((b.x, b.y))
        self.energy_direction.add((b.x, b.y, b.moving))
        type = self.grid[b.y][b.x]
        if type == '/':
            b.moving = LEFT
        elif type == '\\':
            b.moving = RIGHT
        elif type == "-":
            b.moving = RIGHT
            self.beams.append(Beam(b.x, b.y, LEFT))
        return False

# Part 1
input = read_lines("input/day16/input.txt")
sample = read_lines("input/day16/sample.txt")

value = solve_part1(sample)
assert(value == 46)
value = solve_part1(input)
assert(value == -1)

# Part 2
value = solve_part2(sample)
assert(value == -1)
value = solve_part2(input)
assert(value == -1)

from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 16", "Part 1")
def solve_part1(lines: list):
    c = Contraption(lines, Beam(-1, 0, RIGHT))
    while c.energize():
        pass
    return len(c.energized)

@Runner("Day 16", "Part 2")
def solve_part2(lines: list):
    row_count = len(lines)
    col_count = len(lines[0])
    min = row_count * col_count + 1
    for y in range(row_count):
        for x in range(col_count):
            if x == 0:
                print(Beam(x-1, y, RIGHT))
                print(Beam(col_count, y, LEFT))
            if y == 0:
                print(Beam(x, y-1, DOWN))
                print(Beam(x, row_count, UP))
    return 0            

RIGHT = "R"
LEFT = "L"
UP = "U"
DOWN = "D"

class Beam:
    def __init__(self, x: int, y: int, dir: str) -> None:
        self.x = x
        self.y = y
        self.moving = dir
        
    def __repr__(self) -> str:
        return str((self.x, self.y, self.moving))
    
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
                prune = self.__move_beam_right(beam)
            elif beam.moving == LEFT:
                prune = self.__move_beam_left(beam)
            elif beam.moving == UP:
                prune = self.__move_beam_up(beam)
            elif beam.moving == DOWN:
                prune = self.__move_beam_down(beam)
            if prune:
                prune_idxs.append(i)
        for i in range(len(prune_idxs)-1, -1, -1):
            self.beams.pop(prune_idxs[i])
        return len(self.energy_direction) != energy_before
    
    def __move_beam_right(self, b: Beam) -> bool:
        if b.x + 1 == self.col_count:
            return True
        b.x += 1
        
        locdir = (b.x, b.y, b.moving)
        if locdir in self.energy_direction:
            return True
        self.energized.add((b.x, b.y))
        self.energy_direction.add(locdir)
        
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
            return True
        b.x -= 1
        
        locdir = (b.x, b.y, b.moving)
        if locdir in self.energy_direction:
            return True
        self.energized.add((b.x, b.y))
        self.energy_direction.add(locdir)
        
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
            return True
        b.y -= 1
        
        locdir = (b.x, b.y, b.moving)
        if locdir in self.energy_direction:
            return True
        self.energized.add((b.x, b.y))
        self.energy_direction.add(locdir)
        
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
            return True
        b.y += 1
        
        locdir = (b.x, b.y, b.moving)
        if locdir in self.energy_direction:
            return True
        self.energized.add((b.x, b.y))
        self.energy_direction.add(locdir)
        
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
assert(value == 8146)

# Part 2
value = solve_part2(sample)
assert(value == -1)
value = solve_part2(input)
assert(value == -1)

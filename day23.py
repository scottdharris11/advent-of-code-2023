from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 23", "Part 1")
def solve_part1(lines: list):
    island = Island(lines, True)
    return max_hike(island)

@Runner("Day 23", "Part 2")
def solve_part2(lines: list):
    island = Island(lines, False)
    return max_hike(island)

class Island:
    def __init__(self, lines: list[str], onlydown: bool) -> None:
        self.grid = lines
        self.row_count = len(lines)
        self.col_count = len(lines[0])
        self.start = (1, 0)
        self.onlydown = onlydown
        self.moves_cache = {}
        
    def moves_from(self, current: tuple[int]) -> list[tuple[int]]:
        if current in self.moves_cache:
            return self.moves_cache[current]
        moves = []
        for move in [(1,0,">"), (-1,0,"<"), (0,1,"v"), (0,-1,"^")]:
            x = move[0] + current[0]
            y = move[1] + current[1]
            next = self.grid[y][x]
            if next == "#":
                continue
            if self.onlydown and (next != "." and next != move[2]):
                continue
            moves.append((x, y))
        self.moves_cache[current] = moves
        return moves
    
    def path_end(self, current: tuple[int]) -> bool:
        return current[1] == self.row_count - 1

class Hike:
    def __init__(self, steps: list[tuple[int]]) -> None:
        self.steps = steps
        self.ss = set(steps)
        self.done = False
        self.goal = False
        self.current = steps[-1]
    
    def copy(self) -> "Hike":
        return Hike(self.steps[:])
        
    def already_been(self, loc: tuple[int]) -> bool:
        return loc in self.ss
    
    def step(self, loc: tuple[int]) -> None:
        self.steps.append(loc)
        self.ss.add(loc)
        self.current = loc

def max_hike(island: Island) -> int:
    hikes = [Hike([island.start])]
    alldone = False
    steps = []
    while not alldone:
        altpaths = []
        for hike in hikes:
            if hike.done:
                continue
            altpaths.extend(take_hike(island, hike))
            if hike.goal:
                steps.append(len(hike.steps)-1)
        hikes.extend(altpaths)
        if len(altpaths) == 0:
            alldone = True
    return max(steps)

def take_hike(island: Island, hike: Hike) -> list[Hike]:
    altpaths = []
    while True:
        # check to see if we are done
        if island.path_end(hike.current):
            hike.done = True
            hike.goal = True
            return altpaths
        
        # next moves
        moves = island.moves_from(hike.current)
        locations = []
        for move in moves:
            if not hike.already_been(move):
                locations.append(move)
        if len(locations) == 0:
            hike.done = True
            return altpaths
        
        # spawn new hikes for move choices
        for i in range(1, len(locations)):
            nhike = hike.copy()
            nhike.step(locations[i])
            altpaths.append(nhike)
        hike.step(locations[0])

# Part 1
input = read_lines("input/day23/input.txt")
sample = read_lines("input/day23/sample.txt")

value = solve_part1(sample)
assert(value == 94)
value = solve_part1(input)
assert(value == 2030)

# Part 2
value = solve_part2(sample)
assert(value == 154)
value = solve_part2(input)
assert(value == -1)

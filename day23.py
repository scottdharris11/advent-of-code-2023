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

class Path:
    def __init__(self, start: tuple[int], end: tuple[int], steps: int) -> None:
        self.start = start
        self.end = end
        self.steps = steps
        
    def __repr__(self) -> str:
        return str((self.start, self.end, self.steps))
    
class Island:
    def __init__(self, lines: list[str], onlydown: bool) -> None:
        self.grid = lines
        self.row_count = len(lines)
        self.col_count = len(lines[0])
        self.start = (1, 0)
        self.onlydown = onlydown
        self.graph = {}
        
        unexplored = [(self.start,[self.start])]
        while len(unexplored) > 0:
            explore = unexplored.pop()
            if explore[0] in self.graph:
                continue
            self.graph[explore[0]] = []
            for path in explore[1]:
                unexplored.append(self.expand_path(explore[0], path))
    
    def expand_path(self, point: tuple[int], start: tuple[int]) -> (tuple[int], list[tuple[int]]):
        prev = point
        current = start
        steps = 1
        while True:
            moves = []
            count = 0
            for move in [(1,0,">"), (-1,0,"<"), (0,1,"v"), (0,-1,"^")]:
                x = move[0] + current[0]
                y = move[1] + current[1]
                if prev[0] == x and prev[1] == y:
                    continue
                next = self.grid[y][x]
                if next == "#":
                    continue
                if self.onlydown and (next != "." and next != move[2]):
                    continue
                moves.append((x, y))
                count += 1
            if count == 0 or count > 1:
                # found decision point (or end), record path to all and schedule for expansion
                self.graph[point].append(Path(point, current, steps))
                return current, moves
            steps += 1
            prev = current
            current = moves[0]
            if moves[0][1] == self.row_count -1:
                # reached goal, treat as point
                self.graph[point].append(Path(point, current, steps))
                return current, []
    
    def paths_from(self, current: tuple[int]) -> list[Path]:
        return self.graph[current]
        
    def path_end(self, current: tuple[int]) -> bool:
        return current[1] == self.row_count - 1

class Hike:
    def __init__(self) -> None:
        self.points = []
        self.current = None
        self.steps = 0
        self.done = False
        self.goal = False
    
    def copy(self) -> "Hike":
        n = Hike()
        n.points = self.points.copy()
        n.steps = self.steps
        return n
        
    def already_been(self, path: Path) -> bool:
        return path.end in self.points
    
    def take(self, path: Path) -> None:
        self.points.append(path.end)
        self.steps += path.steps
        self.current = path.end

def max_hike(island: Island) -> int:
    start = Hike()
    start.take(Path(island.start, island.start, 0))
    active = [start]
    max_steps = 0
    while len(active) > 0:
        hike = active.pop()
        active.extend(take_hike(island, hike))
        if hike.goal:
            max_steps = max(max_steps, hike.steps-1)
    return max_steps

def take_hike(island: Island, hike: Hike) -> list[Hike]:
    altpaths = []
    while True:
        # check to see if we are done
        if island.path_end(hike.current):
            hike.done = True
            hike.goal = True
            return altpaths
        
        # find next paths
        paths = island.paths_from(hike.current)
        go = []
        for path in paths:
            if not hike.already_been(path):
                go.append(path)
        paths = go
        if len(paths) == 0:
            hike.done = True
            return altpaths
        
        # spawn new hikes for path choices
        for i in range(1, len(paths)):
            nhike = hike.copy()
            nhike.take(paths[i])
            altpaths.append(nhike)
        hike.take(paths[0])

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
assert(value > 5834)

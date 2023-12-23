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
        
        unexplored = [self.start]
        explored = set()
        while len(unexplored) > 0:
            point = unexplored.pop()
            if point in explored:
                continue
            explored.add(point)
            for move in self.__moves_from(point, point):
                next = self.__expand_path(point, move)
                if next == None:
                    continue
                unexplored.append(next)
    
    def __moves_from(self, current: tuple[int], prev: tuple[int]) -> list[tuple[int]]:
        moves = []
        for move in [(1,0,">"), (-1,0,"<"), (0,1,"v"), (0,-1,"^")]:
            x = move[0] + current[0]
            y = move[1] + current[1]
            if x < 0 or x == self.col_count or y < 0 or y == self.row_count:
                continue
            if prev[0] == x and prev[1] == y:
                continue
            next = self.grid[y][x]
            if next == "#":
                continue
            if self.onlydown and (next != "." and next != move[2]):
                continue
            moves.append((x, y))
        return moves
    
    def __expand_path(self, point: tuple[int], start: tuple[int]) -> tuple[int]:
        prev = point
        current = start
        steps = 1
        while True:
            moves = self.__moves_from(current, prev)
            count = len(moves)
            if count == 0:
                # dead end
                return None
            if count > 1:
                # found decision point (or end), record path to all and schedule for expansion
                self.__add_path(Path(point, current, steps))
                return current
            steps += 1
            prev = current
            current = moves[0]
            if moves[0][1] == self.row_count -1:
                # reached goal, treat as point
                self.__add_path(Path(point, current, steps))
                return current
            
    def __add_path(self, path: Path) -> None:
        if path.start not in self.graph:
            self.graph[path.start] = []
        self.graph[path.start].append(path)
    
    def paths_from(self, current: tuple[int]) -> list[Path]:
        return self.graph[current]
        
    def path_end(self, current: tuple[int]) -> bool:
        return current[1] == self.row_count - 1

class Hike:
    def __init__(self) -> None:
        self.points = set()
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
        self.points.add(path.end)
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
            max_steps = max(max_steps, hike.steps)
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
assert(value == 6390)

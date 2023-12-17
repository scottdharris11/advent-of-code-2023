from utilities.data import read_lines
from utilities.runner import Runner
from utilities.search import Search, Searcher, SearchMove

@Runner("Day 17", "Part 1")
def solve_part1(lines: list):
    city = City(lines)
    ps = PathSearcher(city)
    s = Search(ps)
    solution = s.best(SearchMove(0, PathState((0,0), [(0,0)])))
    if solution == None:
        return -1
    return solution.cost

@Runner("Day 17", "Part 2")
def solve_part2(lines: list):
    return -1

class City:
    def __init__(self, lines: list[str]) -> None:
        self.heat_grid = []
        for line in lines:
            row = []
            for c in line:
                row.append(int(c))
            self.heat_grid.append(row)
        self.row_count = len(lines)
        self.col_count = len(lines[0])
        self.factory = (self.col_count - 1, self.row_count - 1)
    
    def is_factory(self, point: tuple[int]) -> bool:
        return point == self.factory
    
    def moves_from(self, point: tuple[int]) -> list[tuple[int]]:
        possible = []
        if point[0] + 1 < self.col_count:
            possible.append((1, 0))
        if point[0] - 1 >= 0:
            possible.append((-1, 0))
        if point[1] + 1 < self.row_count:
            possible.append((0, 1))
        if point[1] - 1 >= 0:
            possible.append((0, -1))
        return possible
    
    def heat_cost(self, point: tuple[int]) -> int:
        return self.heat_grid[point[1]][point[0]]
    
    def distance_from_factory(self, point: tuple[int]) -> int:
        return abs(point[0] - self.factory[0]) + abs(point[1] - self.factory[1])

class PathState:
    def __init__(self, point: tuple[int], prev: list[tuple[int]]) -> None:
        self.point = point
        self.prev = prev
    
    def __repr__(self) -> str:
        return str((self.point, self.prev))
    
    def __hash__(self) -> int:
        h = hash(self.point)
        for i, p in enumerate(self.prev):
            h += (i+1) * hash(p)
        return h
    
    def __eq__(self, other: object) -> bool:
        if other == None:
            return False
        if self.point != other.point:
            return False
        if len(self.prev) != len(other.prev):
            return False
        for i in range(len(self.prev)):
            if self.prev[i] != other.prev[i]:
                return False
        return True
    
    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)
    
    def move_valid(self, dir: tuple[int]) -> bool:
        last = self.prev[-1]
        if last[0] != 0 and last[0] * -1 == dir[0]:
            return False
        if last[1] != 0 and last[1] * -1 == dir[1]:
            return False
        if len(self.prev) < 3:
            return True
        for p in self.prev:
            if p != dir:
                return True
        return False
    
    def state_for_move(self, dir: tuple[int]) -> "PathState":
        nprev = self.prev[:]
        nprev.append(dir)
        if len(nprev) > 3:
            nprev.pop(0)
        npoint = (self.point[0] + dir[0], self.point[1] + dir[1])
        return PathState(npoint, nprev)
        
    
class PathSearcher(Searcher):
    def __init__(self, city: City) -> None:
        self.city = city
        
    def is_goal(self, state: PathState) -> bool:
        return self.city.is_factory(state.point)
    
    def possible_moves(self, state: PathState) -> list[SearchMove]:
        moves = set()
        possible = self.city.moves_from(state.point)
        for p in possible:
            if state.move_valid(p):
                move = state.state_for_move(p)
                cost = self.city.heat_cost(move.point)
                moves.add(SearchMove(cost, move))
        return moves
    
    def distance_from_goal(self, state: PathState) -> int:
        return self.city.distance_from_factory(state.point)

# Part 1
input = read_lines("input/day17/input.txt")
sample = read_lines("input/day17/sample.txt")

value = solve_part1(sample)
assert(value == 102)
value = solve_part1(input)
assert(value == 767)

# Part 2
value = solve_part2(sample)
assert(value == 102)
value = solve_part2(input)
assert(value == -1)

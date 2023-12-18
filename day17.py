from utilities.data import read_lines
from utilities.runner import Runner
from utilities.search import Search, Searcher, SearchMove

@Runner("Day 17", "Part 1")
def solve_part1(lines: list):
    city = City(lines)
    ps = PathSearcher(city)
    s = Search(ps)
    solution = s.best(SearchMove(0, CrucibleState((0,0), (0, 0), 1)))
    if solution == None:
        return -1
    return solution.cost

@Runner("Day 17", "Part 2")
def solve_part2(lines: list):
    city = City(lines)
    ps = PathSearcher(city)
    s = Search(ps)
    solution = s.best(SearchMove(0, UltraCrucibleState((0,0), (0, 0), 1)))
    if solution == None:
        return -1
    return solution.cost

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

class CrucibleState:
    def __init__(self, point: tuple[int], dir: tuple[int], times: int) -> None:
        self.point = point
        self.lastdir = dir
        self.times = times
    
    def __repr__(self) -> str:
        return str((self.point, self.lastdir, self.times))
    
    def __hash__(self) -> int:
        h = hash(self.point)
        h += hash(self.lastdir) * self.times
        return h
    
    def __eq__(self, other: object) -> bool:
        if other == None:
            return False
        if self.point != other.point:
            return False
        if self.lastdir != other.lastdir:
            return False
        if self.times != other.times:
            return False
        return True
    
    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)
    
    def move_valid(self, dir: tuple[int], _: City) -> bool:
        # can't turn around
        last = self.lastdir
        if last[0] != 0 and last[0] * -1 == dir[0]:
            return False
        if last[1] != 0 and last[1] * -1 == dir[1]:
            return False
        
        # can't move in same direction more than three times
        if dir == self.lastdir and self.times == 3:
            return False
        return True
    
    def state_for_move(self, dir: tuple[int]) -> "CrucibleState":
        npoint = (self.point[0] + dir[0], self.point[1] + dir[1])
        ntimes = 1
        if self.lastdir == dir:
            ntimes += self.times
        return CrucibleState(npoint, dir, ntimes)

class UltraCrucibleState(CrucibleState):
    def move_valid(self, dir: tuple[int], city: City) -> bool:
        # can't turn around
        last = self.lastdir
        if last[0] != 0 and last[0] * -1 == dir[0]:
            return False
        if last[1] != 0 and last[1] * -1 == dir[1]:
            return False
        
        # if last initial state, then good
        if last == (0, 0):
            return True
        
        # must maintain direction for four blocks
        if dir != last and self.times < 4:
            return False
                
        # can't do more than 10 consecutive
        consecutive = 1
        if dir == last:
            consecutive = self.times + 1
        if consecutive == 10:
            return False
            
        # must be able to do at least four blocks
        need = 4 - consecutive + 1
        possible = True
        p = self.point
        for _ in range(need):
            moves = city.moves_from(p)
            if dir not in moves:
                possible = False
                break
            p = (p[0] + dir[0], p[1] + dir[1])
        return possible
    
    def state_for_move(self, dir: tuple[int]) -> "UltraCrucibleState":
        npoint = (self.point[0] + dir[0], self.point[1] + dir[1])
        ntimes = 1
        if self.lastdir == dir:
            ntimes += self.times
        return UltraCrucibleState(npoint, dir, ntimes)
    
class PathSearcher(Searcher):
    def __init__(self, city: City) -> None:
        self.city = city
        
    def is_goal(self, state: CrucibleState) -> bool:
        return self.city.is_factory(state.point)
    
    def possible_moves(self, state: CrucibleState) -> list[SearchMove]:
        moves = set()
        possible = self.city.moves_from(state.point)
        for p in possible:
            if state.move_valid(p, self.city):
                move = state.state_for_move(p)
                cost = self.city.heat_cost(move.point)
                moves.add(SearchMove(cost, move))
        return moves
    
    def distance_from_goal(self, state: CrucibleState) -> int:
        return self.city.distance_from_factory(state.point)

# Part 1
input = read_lines("input/day17/input.txt")
sample = read_lines("input/day17/sample.txt")
sample2 = read_lines("input/day17/sample2.txt")

value = solve_part1(sample)
assert(value == 102)
value = solve_part1(input)
assert(value == 767)

# Part 2
value = solve_part2(sample)
assert(value == 94)
value = solve_part2(sample2)
assert(value == 71)
value = solve_part2(input)
assert(value < 934)

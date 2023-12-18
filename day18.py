from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 18", "Part 1")
def solve_part1(lines: list):
    plan = DigPlan(lines)
    #print(plan)
    return plan.cubic_meters()

@Runner("Day 18", "Part 2")
def solve_part2(lines: list):
    return -1

RIGHT = 'R'
LEFT = 'L'
UP = 'U'
DOWN = 'D'
START = 'S'
VERTICAL = '|'
HORIZONTAL = "-"
NORTH_TO_EAST = "L"
NORTH_TO_WEST = "J"
SOUTH_TO_WEST = "7"
SOUTH_TO_EAST = "F"

JOINT_MAPPINGS = {
    DOWN : { DOWN: VERTICAL, UP : VERTICAL, RIGHT: NORTH_TO_EAST, LEFT : NORTH_TO_WEST },
    UP : { DOWN: VERTICAL, UP : VERTICAL, RIGHT : SOUTH_TO_EAST, LEFT : SOUTH_TO_WEST },
    RIGHT : { DOWN : SOUTH_TO_WEST, UP : NORTH_TO_WEST, RIGHT : HORIZONTAL, LEFT : HORIZONTAL },
    LEFT : { DOWN : SOUTH_TO_EAST, UP : NORTH_TO_EAST, RIGHT : HORIZONTAL, LEFT : HORIZONTAL },
}

class DigInstruction:
    def __init__(self, line: str) -> None:
        s = line.split()
        self.dir = s[0]
        self.steps = int(s[1])
        self.color = s[2][1:-1]
    
    def __repr__(self) -> str:
        return str((self.dir, self.steps, self.color))

class DigPoint:
    def __init__(self, x: int, y: int) -> None:
        self.point = (x, y)

    def __repr__(self) -> str:
        return str(self.point)
    
    def __hash__(self) -> int:
        return hash(self.point)
    
    def __eq__(self, other: object) -> bool:
        if other == None:
            return False
        p = other
        if type(p) == "DigPoint":
            p = other.point
        return self.point == p
    
    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

class DigPlan:
    def __init__(self, lines: list[str]) -> None:
        # apply instructions
        self.current = (0,0)
        self.edges = {}
        self.edges[DigPoint(0,0)] = START
        self.rowmin = 0
        self.rowmax = 0
        self.colmin = 0
        self.colmax = 0
        
        for i, line in enumerate(lines):
            di = DigInstruction(line)
            self.add_instruction(di)
            if i == 0:
                self.edges[(0,0)] = di.dir
        
    def __repr__(self) -> str:
        output = ""
        
        columns = abs(self.colmin - self.colmax)
        colsplit = int(columns / 2) + self.colmin
        if columns < 40:
            colsplit = self.colmax + 1
        
        for r in range(self.rowmin, self.rowmax+1):
            for c in range(self.colmin, colsplit):
                p = (c, r)
                if p in self.edges:
                    output += self.edges[p]
                else:
                    output += "."
            output += ">" + str(r) + ">\n"
            
        output += "\n\n\n\n"
        for r in range(self.rowmin, self.rowmax+1):
            output += ">" + str(r) + ">"
            for c in range(colsplit, self.colmax+1):
                p = (c, r)
                if p in self.edges:
                    output += self.edges[p]
                else:
                    output += "."
            output += "\n"
            
        return output
    
    def cubic_meters(self) -> int:
        cubes = 0
        for r in range(self.rowmin, self.rowmax+1):
            for c in range(self.colmin, self.colmax+1):
                point = (c, r)
                if point in self.edges:
                    cubes += 1
                    continue
                inside = True
                for adjust in [[(1, 0), (self.colmax+1, point[1])], [(-1, 0), (self.colmin-1, point[1])], [(0, 1), (point[0], self.rowmax+1)], [(0, -1), (point[0], self.rowmin-1)]]:
                    edgex = self.__edge_crossings(point, adjust[0], adjust[1])
                    if edgex == 0 or edgex % 2 == 0:
                        inside = False
                        break
                if inside:
                    cubes += 1
        return cubes
    
    def __edge_crossings(self, point: tuple[int], adjust: tuple[int], stop: int):
        crossings = 0
        elbow = ""
        while point != stop:
            if point in self.edges:
                ptype = self.edges[point]
                if ptype == HORIZONTAL or ptype == VERTICAL:
                    if elbow == "":
                        crossings += 1
                elif elbow == "":
                    elbow = ptype
                else:
                    if ((elbow == SOUTH_TO_WEST and ptype == NORTH_TO_EAST) or 
                        (elbow == SOUTH_TO_EAST and ptype == NORTH_TO_WEST) or
                        (elbow == NORTH_TO_EAST and ptype == SOUTH_TO_WEST) or
                        (elbow == NORTH_TO_WEST and ptype == SOUTH_TO_EAST)):
                        crossings += 1
                    elbow = ""
            point = (point[0] + adjust[0], point[1] + adjust[1])
        return crossings
    
    def add_instruction(self, i: DigInstruction) -> None:
        point = None
        if i.dir == "R":
            point = (self.current[0] + i.steps, self.current[1])
            self._add_range(point[1], range(self.current[0], point[0]+1), HORIZONTAL, i.dir)
        elif i.dir == "L":
            point = (self.current[0] - i.steps, self.current[1])
            self._add_range(point[1], range(self.current[0], point[0]-1, -1), HORIZONTAL, i.dir)
        elif i.dir == "U":
            point = (self.current[0], self.current[1] - i.steps)
            for r in range(self.current[1], point[1]-1, -1):
                dir = VERTICAL
                if r == point[1] or r == self.current[1]:
                    dir = i.dir
                self._add_range(r, range(point[0], point[0]+1), VERTICAL, dir)
        else:
            point = (self.current[0], self.current[1] + i.steps)
            for r in range(self.current[1], point[1]+1, 1):
                dir = VERTICAL
                if r == point[1] or r == self.current[1]:
                    dir = i.dir
                self._add_range(r, range(point[0], point[0]+1), VERTICAL, dir)
        self.current = point
        
    def _add_range(self, y: int, ss: range, edge: str, dir: str) -> None:
        for i in ss:
            dp = DigPoint(i, y)
            if dp in self.edges:
                prevdir = self.edges[dp]
                if y == 0 and i == 0:
                    if prevdir != START:
                        self.edges[dp] = JOINT_MAPPINGS[dir][prevdir]
                else:
                    self.edges[dp] = JOINT_MAPPINGS[prevdir][dir]
            else:
                self.edges[dp] = edge
                if (ss.step == 1 and i == ss.stop - 1) or (ss.step == -1 and i == ss.stop +1):
                    self.edges[dp] = dir
            self.rowmin = min(self.rowmin, y)
            self.rowmax = max(self.rowmax, y)
            self.colmin = min(self.colmin, i)
            self.colmax = max(self.colmax, i)

# Part 1
input = read_lines("input/day18/input.txt")
sample = read_lines("input/day18/sample.txt")

value = solve_part1(sample)
assert(value == 62)
value = solve_part1(input)
assert(value == 47045)

# Part 2
#value = solve_part2(sample)
#assert(value == -1)
#value = solve_part2(input)
#assert(value == -1)

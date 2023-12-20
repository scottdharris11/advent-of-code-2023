from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 18", "Part 1")
def solve_part1(lines: list):
    plan = DigPlan(lines)
    print(plan.row_ranges)
    print(plan.col_ranges)
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
        self.row_ranges = {}
        self.col_ranges = {}
        
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
    
    def vertical(self, row: int, col: int) -> tuple[int]:
        for r in self.col_ranges[col]:
            if r[0] == row:
                return r
    
    def remove_vertical(self, row: int, col: int) -> None:
        for i, r in enumerate(self.col_ranges[col]):
            if r[0] == row:
                self.col_ranges[col].pop(i)
                return
    
    def replace_vertical(self, row: int, col: int, val: tuple[int]) -> None:
        for i, r in enumerate(self.col_ranges[col]):
            if r[0] == row:
                self.col_ranges[col][i] = val
                return
    
    def cubic_meters(self) -> int:
        hkeys = []
        hkeys.extend(self.row_ranges.keys())
        hkeys.sort()
        hkeys.reverse()
        print(hkeys)
        
        cubes = 0
        overlap = 0
        while len(hkeys) > 0:
            # Highest horizontal range
            key = hkeys[-1]
            hrange = self.row_ranges[key][0]
            
            # Get verticals associated and find minimum
            lvert = self.vertical(key, hrange[0])
            rvert = self.vertical(key, hrange[1])
            mvert = lvert
            mincol = hrange[0]
            maxcol = hrange[1]
            if rvert[1] < lvert[1]:
                mvert = rvert
                mincol = hrange[1]
                maxcol = hrange[0]
            
            # add to total cubes
            cubes += (abs(mvert[1] - key) + 1) * (abs(maxcol - mincol) + 1)
            
            # locate horizontal associated with shortest vert
            for i, r in enumerate(self.row_ranges[mvert[1]]):
                if mincol == r[0] and maxcol == r[1]:
                    # min and max columns match the horizontal range
                    # so this is a bottom, remove bottom horizontal
                    self.row_ranges[mvert[1]].pop(i)
                    break
                if mincol == r[0]:
                    # minimum column is moving to the right...adjust
                    # range over to the max column
                    self.row_ranges[mvert[1]][i] = (r[1], maxcol)
                    overlap += maxcol - r[1] + 1
                    break
                elif mincol == r[1]:
                    # minimum column is moving to the left...extend range
                    # to the next horizontal column
                    nhoz = None
                    nidx = -1
                    for n, next in enumerate(self.row_ranges[mvert[1]]):
                        if next[0] > r[1] and (nhoz == None or nhoz[0] > r[1]):
                            nhoz = next
                            nidx = n
                    if nhoz[0] < maxcol:
                        self.row_ranges[mvert[1]][i] = (r[0], nhoz[0])
                    else:
                        self.row_ranges[mvert[1]][i] = (r[0], nhoz[1])
                    self.row_ranges[mvert[1]].pop(nidx)
                    overlap += min(maxcol, nhoz[0]) - mincol + 1
                    break
                
            # remove horizontal range(s) and short vertical(s)
            self.row_ranges[key].pop(0)
            if len(self.row_ranges[key]) == 0:
                self.row_ranges.pop(key)
            
            self.remove_vertical(key, mincol)
            if rvert[1] == lvert[1]:
                self.remove_vertical(key, maxcol)
            else:
                self.replace_vertical(key, maxcol, (mincol, maxcol))
        return cubes - overlap
                
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
            self.__add_horizontal_range(point[1], self.current[0], point[0])
            
        elif i.dir == "L":
            point = (self.current[0] - i.steps, self.current[1])
            self._add_range(point[1], range(self.current[0], point[0]-1, -1), HORIZONTAL, i.dir)
            self.__add_horizontal_range(point[1], point[0], self.current[0])
            
        elif i.dir == "U":
            point = (self.current[0], self.current[1] - i.steps)
            for r in range(self.current[1], point[1]-1, -1):
                dir = VERTICAL
                if r == point[1] or r == self.current[1]:
                    dir = i.dir
                self._add_range(r, range(point[0], point[0]+1), VERTICAL, dir)
            self.__add_vertical_range(point[0], point[1], self.current[1])
            
        else:
            point = (self.current[0], self.current[1] + i.steps)
            for r in range(self.current[1], point[1]+1, 1):
                dir = VERTICAL
                if r == point[1] or r == self.current[1]:
                    dir = i.dir
                self._add_range(r, range(point[0], point[0]+1), VERTICAL, dir)
            self.__add_vertical_range(point[0], self.current[1], point[1])
            
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
            
    def __add_horizontal_range(self, row: int, start: int, stop: int) -> None:
        ranges = self.row_ranges.get(row, [])
        ranges.append((start, stop))
        self.row_ranges[row] = ranges
        
    def __add_vertical_range(self, col: int, start: int, stop: int) -> None:
        ranges = self.col_ranges.get(col, [])
        ranges.append((start, stop))
        self.col_ranges[col] = ranges

# Part 1
input = read_lines("input/day18/input.txt")
sample = read_lines("input/day18/sample.txt")

value = solve_part1(sample)
assert(value == 62)
#value = solve_part1(input)
#assert(value == 47045)

# Part 2
#value = solve_part2(sample)
#assert(value == -1)
#value = solve_part2(input)
#assert(value == -1)

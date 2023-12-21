from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 18", "Part 1")
def solve_part1(lines: list):
    plan = DigPlan(lines)
    return plan.cubic_meters()

@Runner("Day 18", "Part 2")
def solve_part2(lines: list):
    return -1

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
        self.row_ranges = {}
        self.col_ranges = {}
        self.current = (0,0)
        
        for i, line in enumerate(lines):
            di = DigInstruction(line)
            self.add_instruction(di)
        
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
    
    def horizontal(self, row: int, col: int) -> tuple[int]:
        for r in self.row_ranges[row]:
            if r[0] == col or r[1] == col:
                return r
    
    def replace_horizontal(self, row: int, col: int, val: tuple[int]) -> None:
        for i, r in enumerate(self.row_ranges[row]):
            if r[0] == col or r[1] == col:
                self.row_ranges[row][i] = val
                return
    
    def remove_horizontal(self, row: int, col: int) -> None:
        for i, r in enumerate(self.row_ranges[row]):
            if r[0] == col or r[1] == col:
                self.row_ranges[row].pop(i)
                return
            
    def vertical(self, row: int, col: int) -> tuple[int]:
        for r in self.col_ranges[col]:
            if r[0] == row:
                return r
        print("vertical not found at row %d, col %d" % (row, col))
    
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
            minvert = lvert
            maxvert = rvert
            mincol = hrange[0]
            maxcol = hrange[1]
            if rvert[1] < lvert[1]:
                minvert = rvert
                maxvert = lvert
                mincol = hrange[1]
                maxcol = hrange[0]
            
            # add to total cubes
            cubes += (abs(minvert[1] - key) + 1) * (abs(maxcol - mincol) + 1)
            
            # locate horizontal associated with shortest vert
            hoz = self.horizontal(minvert[1], mincol)
            if minvert[1] == maxvert[1]:
                if mincol == hoz[0] and maxcol == hoz[1]:
                    # min and max columns match the horizontal range
                    # so this is a bottom, remove bottom horizontal
                    self.remove_horizontal(minvert[1], mincol)
                else:
                    # verticals are equal, merge left horizontal with right
                    hoz2 = self.horizontal(maxvert[1], maxcol)
                    begin = hoz[1]
                    obegin = hoz[1]
                    if hoz[0] < mincol:
                        begin = hoz[0]
                        obegin = mincol
                    end = hoz2[1]
                    oend = maxcol
                    if hoz2[0] < maxcol:
                        end = hoz2[0]
                        oend = hoz2[0]
                    self.replace_horizontal(minvert[1], mincol, (begin, end))
                    self.remove_horizontal(maxvert[1], maxcol)
                    overlap += oend - obegin + 1
            elif mincol == hoz[0]:
                # minimum column is moving to the right...adjust
                # range over to the max column
                if lvert[1] == minvert[1]:
                    self.replace_horizontal(minvert[1], mincol, (hoz[1], maxcol))
                    overlap += maxcol - hoz[1] + 1
                else:
                    self.replace_horizontal(minvert[1], mincol, (maxcol, hoz[1]))
                    overlap += maxcol - mincol + 1
            elif mincol == hoz[1]:
                # minimum column is moving to the left...adjust
                # range over to the max column
                if lvert[1] == minvert[1]:
                    self.replace_horizontal(minvert[1], mincol, (hoz[0], maxcol))
                    overlap += maxcol - hoz[1] + 1
                else:
                    self.replace_horizontal(minvert[1], mincol, (maxcol, hoz[0]))
                    overlap += hoz[0] - maxcol + 1
                
            # remove horizontal range(s) and short vertical(s)
            self.row_ranges[key].pop(0)
            if len(self.row_ranges[key]) == 0:
                self.row_ranges.pop(key)
                hkeys.remove(key)
            if len(self.row_ranges[minvert[1]]) == 0:
                self.row_ranges.pop(minvert[1])
                hkeys.remove(minvert[1])
            
            self.remove_vertical(key, mincol)
            if rvert[1] == lvert[1]:
                self.remove_vertical(key, maxcol)
            else:
                self.replace_vertical(key, maxcol, (minvert[1], maxvert[1]))
        return cubes - overlap
   
    def add_instruction(self, i: DigInstruction) -> None:
        point = None
        if i.dir == "R":
            point = (self.current[0] + i.steps, self.current[1])
            self.__add_horizontal_range(point[1], self.current[0], point[0])
            
        elif i.dir == "L":
            point = (self.current[0] - i.steps, self.current[1])
            self.__add_horizontal_range(point[1], point[0], self.current[0])
            
        elif i.dir == "U":
            point = (self.current[0], self.current[1] - i.steps)
            self.__add_vertical_range(point[0], point[1], self.current[1])
            
        else:
            point = (self.current[0], self.current[1] + i.steps)
            self.__add_vertical_range(point[0], self.current[1], point[1])
        self.current = point
            
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
value = solve_part1(input)
assert(value == 47045)

# Part 2
#value = solve_part2(sample)
#assert(value == -1)
#value = solve_part2(input)
#assert(value == -1)

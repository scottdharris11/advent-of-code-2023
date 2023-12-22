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
    
    def horizontal(self, row: int, col: int) -> tuple[int]:
        print("getting horizontal at row %d, col %d" % (row, col))
        for r in self.row_ranges[row]:
            if r[0] == col or r[1] == col:
                return r
        print("horizontal not found at row %d, col %d" % (row, col))
    
    def replace_horizontal(self, row: int, col: int, val: tuple[int]) -> None:
        print("Replacing horizontal: %s" % str((row, col, val)))
        if val == (4,322):
            hkeys = []
            hkeys.extend(self.row_ranges.keys())
            hkeys.sort()
            hkeys.reverse()
            print("rows")
            for hkey in hkeys:
                print("%d: %s"%(hkey, self.row_ranges[hkey]))
            vkeys = []
            vkeys.extend(self.col_ranges.keys())
            vkeys.sort()
            vkeys.reverse
            print("cols")
            for vkey in vkeys:
                print("%d: %s"%(vkey, self.col_ranges[vkey]))
            exit()
        if val[0] > val[1]:
            exit()
        for i, r in enumerate(self.row_ranges[row]):
            if r[0] == col or r[1] == col:
                self.row_ranges[row][i] = val
                return
    
    def remove_horizontal(self, row: int, col: int) -> None:
        print("Removing horizontal: %s" % str((row, col)))
        for i, r in enumerate(self.row_ranges[row]):
            if r[0] == col or r[1] == col:
                self.row_ranges[row].pop(i)
                return
            
    def vertical(self, row: int, col: int) -> tuple[int]:
        print("getting vertical at row %d, col %d" % (row, col))
        for r in self.col_ranges[col]:
            if r[0] == row:
                return r
        print("vertical not found at row %d, col %d" % (row, col))
        print(self.col_ranges[col])
    
    def remove_vertical(self, row: int, col: int) -> None:
        print("Removing vertical: %s" % str((row, col)))
        for i, r in enumerate(self.col_ranges[col]):
            if r[0] == row:
                self.col_ranges[col].pop(i)
                return
    
    def replace_vertical(self, row: int, col: int, val: tuple[int]) -> None:
        print("Replacing vertical: %s" % str((row, col, val)))
        for i, r in enumerate(self.col_ranges[col]):
            if r[0] == row:
                self.col_ranges[col][i] = val
                return
    
    def cubic_meters(self) -> int:
        hkeys = []
        hkeys.extend(self.row_ranges.keys())
        hkeys.sort()
        hkeys.reverse()
        print("rows")
        for hkey in hkeys:
            print("%d: %s"%(hkey, self.row_ranges[hkey]))
        vkeys = []
        vkeys.extend(self.col_ranges.keys())
        vkeys.sort()
        vkeys.reverse
        print("cols")
        for vkey in vkeys:
            print("%d: %s"%(vkey, self.col_ranges[vkey]))
        
        
        cubes = 0
        overlap = 0
        while len(hkeys) > 0:
            print(self.col_ranges[-21])
            # Highest horizontal range
            key = hkeys[-1]
            print(key)
            hrange = self.row_ranges[key][0]
            
            # Get verticals associated and find minimum
            print(hrange)
            lvert = self.vertical(key, hrange[0])
            rvert = self.vertical(key, hrange[1])
            print("lvert: %s, rvert: %s"%(lvert, rvert))
            minvert = lvert
            maxvert = rvert
            mincol = hrange[0]
            maxcol = hrange[1]
            if rvert[1] < lvert[1]:
                minvert = rvert
                maxvert = lvert
                mincol = hrange[1]
                maxcol = hrange[0]
            print("min: %d, max: %d"%(mincol,maxcol))
            print("minvert: %s, maxvert: %s"%(minvert, maxvert))
            
            # add to total cubes
            cubes += (abs(minvert[1] - key) + 1) * (abs(maxcol - mincol) + 1)
            
            # locate horizontal associated with shortest vert
            hoz = self.horizontal(minvert[1], mincol)
            print("horizontal at shortest vert %s"%str(hoz))
            if minvert[1] == maxvert[1]:
                if mincol == hoz[0] and maxcol == hoz[1]:
                    # min and max columns match the horizontal range
                    # so this is a bottom, remove bottom horizontal
                    self.remove_horizontal(minvert[1], mincol)
                else:
                    # verticals are equal, merge left horizontal with right
                    hoz2 = self.horizontal(maxvert[1], maxcol)
                    print("other horizontal: %s"%str(hoz2))
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
                    overlap += abs(oend - obegin) + 1
            elif mincol == hoz[0]:
                # minimum column is moving to the right...adjust
                # range over to the max column
                if lvert[1] == minvert[1]:
                    self.replace_horizontal(minvert[1], mincol, (hoz[1], maxcol))
                    overlap += abs(maxcol - hoz[1]) + 1
                else:
                    self.replace_horizontal(minvert[1], mincol, (maxcol, hoz[1]))
                    overlap += abs(maxcol - mincol)+ 1
            elif mincol == hoz[1]:
                # minimum column is moving to the left...adjust
                # range over to the max column
                if lvert[1] == minvert[1]:
                    self.replace_horizontal(minvert[1], mincol, (hoz[0], maxcol))
                    overlap += abs(maxcol - hoz[1]) + 1
                else:
                    self.replace_horizontal(minvert[1], mincol, (maxcol, hoz[0]))
                    overlap += abs(hoz[0] - maxcol) + 1
                
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

#value = solve_part1(sample)
#assert(value == 62)
value = solve_part1(input)
assert(value == 47045)

# Part 2
#value = solve_part2(sample)
#assert(value == -1)
#value = solve_part2(input)
#assert(value == -1)

from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 18", "Part 1")
def solve_part1(lines: list):
    plan = DigPlan(lines, False)
    return plan.cubic_meters()

@Runner("Day 18", "Part 2")
def solve_part2(lines: list):
    plan = DigPlan(lines, True)
    return plan.cubic_meters()

DIR_FROM_HEX = {0: "R", 1: "D", 2: "L", 3: "U"}

class DigInstruction:
    def __init__(self, line: str, useColor: bool) -> None:
        s = line.split()
        if useColor:
            color = s[2][1:-1]
            self.steps = int(color[1:-1], 16)
            self.dir = DIR_FROM_HEX[int(color[-1])]
        else:
            self.dir = s[0]
            self.steps = int(s[1])
    
    def __repr__(self) -> str:
        return str((self.dir, self.steps))

class DigPlan:
    def __init__(self, lines: list[str], useHex: bool) -> None:
        self.current = (0,0)
        self.vertices = [self.current]
        self.boundary_cubes = 0
        for line in lines:
            di = DigInstruction(line, useHex)
            self.__add_instruction(di)
        
    def cubic_meters(self) -> int:
        # went round and round here trying to calculate by breaking
        # pologon in rectanges.  got close but too many edge cases to 
        # deal with. Credit to Chris Vogel for finding these theorm's 
        # to make this a pretty simple conversion.
        
        # shoelace formula to calculate total area
        #  (https://en.wikipedia.org/wiki/Shoelace_formula)
        area = 0
        for i in range(len(self.vertices)-2):
            j = i + 1
            area += self.vertices[i][0] * self.vertices[j][1]
            area -= self.vertices[i][1] * self.vertices[j][0]
        area /= 2
        
        # picks theorm to deterrmine inner cube count
        #  (https://en.wikipedia.org/wiki/Pick%27s_theorem)
        inner = int(area - (self.boundary_cubes/2) + 1)
        
        # total cubes is inner cubes plus boundary
        return inner + self.boundary_cubes
   
    def __add_instruction(self, i: DigInstruction) -> None:
        point = None
        if i.dir == "R":
            point = (self.current[0] + i.steps, self.current[1])
        elif i.dir == "L":
            point = (self.current[0] - i.steps, self.current[1])
        elif i.dir == "U":
            point = (self.current[0], self.current[1] - i.steps)   
        else:
            point = (self.current[0], self.current[1] + i.steps)
        self.current = point
        self.vertices.append(point)
        self.boundary_cubes += i.steps

# Part 1
input = read_lines("input/day18/input.txt")
sample = read_lines("input/day18/sample.txt")

value = solve_part1(sample)
assert(value == 62)
value = solve_part1(input)
assert(value == 47045)

# Part 2
value = solve_part2(sample)
assert(value == 952408144115)
value = solve_part2(input)
assert(value == 147839570293376)

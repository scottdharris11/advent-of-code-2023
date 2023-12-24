import math
from utilities.data import read_lines, parse_integers
from utilities.runner import Runner

@Runner("Day 24", "Part 1")
def solve_part1(lines: list, min, max):
    stones = []
    for line in lines:
        stones.append(HailStone(line))   
    intersect = 0
    for i, stone in enumerate(stones):
        for j in range(i+1, len(stones)):
            s1 = (stone.yIntercept(min), stone.yIntercept(max))
            s2 = (stones[j].yIntercept(min), stones[j].yIntercept(max))
            p = xyIntersect(s1, s2)
            
            # Kick out when:
            # - No intersection
            # - Intersection occured in past
            # - Intersection outside of desired range
            if p == None:
                continue
            if stone.inPast(p) or stones[j].inPast(p):
                continue
            if p[0] < min or p[0] > max or p[1] < min or p[1] > max:
                continue
            
            intersect += 1
    return intersect

@Runner("Day 24", "Part 2")
def solve_part2(lines: list):
    return -1

class HailStone:
    def __init__(self, line: str) -> None:
        s = line.split("@")
        self.location = tuple(parse_integers(s[0], ","))
        self.velocity = tuple(parse_integers(s[1], ","))
        self.slope = self.velocity[1] / self.velocity[0]
        self.slope3d = self.velocity[2] / math.sqrt( (self.velocity[0]**2 + self.velocity[1]**2))
        
    def __repr__(self) -> str:
        return str((self.location, self.velocity))
    
    def yIntercept(self, x: float) -> tuple[float]:
        y = (self.slope * (x - self.location[0])) + self.location[1]
        return (x, y)
    
    def xIntercept(self, y:float) -> tuple[float]:
        x = ((y - self.location[1]) / self.slope) + self.location[0]
        return (x, y)
    
    def inPast(self, p: tuple[float]) -> bool:
        return ((self.velocity[0] < 0 and p[0] > self.location[0]) or
            (self.velocity[0] > 0 and p[0] < self.location[0]) or
            (self.velocity[1] < 0 and p[1] > self.location[1]) or
            (self.velocity[1] > 0 and p[1] < self.location[1]))

# credit this post with code for intersection:
#    https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines
def xyIntersect(line1: tuple[tuple[int]], line2: tuple[tuple[int]]) -> tuple[float]:
    start1 = line1[0]
    end1 = line1[1]
    start2 = line2[0]
    end2 = line2[1]
    
    xdiff = (start1[0] - end1[0], start2[0] - end2[0])
    ydiff = (start1[1] - end1[1], start2[1] - end2[1])
    
    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return None

    d = (det(start1, end1), det(start2, end2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return (x, y)

def xyzIntercept(stone1: HailStone, stone2: HailStone) -> tuple[float]:
    # x1 = locX1 + (alpha * vX1), x2 = locX2 + (beta * vX2)
    # e1:  locX1 + (alpha * vX1) = locX2 + (beta * vX2)
    #      (alpha * vX1) = locX2 + (beta * vX2) - locX1
    #      alpha = (locX2 + (beta * vX2) - locX1) / vX1
    #
    # y1 = locY1 + (alpha * vY1), y2 = locY2 + (beta * vY2)
    # e2:  locY1 + (alpha * vY1) = locY2 + (beta * vY2)
    #      (alpha * vY1) = locY2 + (beta * vY2) - locY1
    #      alpha = (locY2 + (beta * vY2) - locY1) / vY1
    #
    # e1 - e2:
    #      (locX2 + (beta * vX2) - locX1) / vX1 = (locY2 + (beta * vY2) - locY1) / vY1
    #      (locX2 + (beta * vX2) - locX1) * vY1 = (locX2 + (beta * vX2) - locX1) * vX1
    #
    return (0.0,0.0,0.0)

# Part 1
input = read_lines("input/day24/input.txt")
sample = read_lines("input/day24/sample.txt")

value = solve_part1(sample, 7, 24)
assert(value == 2)
value = solve_part1(input, 200000000000000, 400000000000000)
assert(value == 20847)

# Part 2
value = solve_part2(sample)
assert(value == -1)
value = solve_part2(input)
assert(value == -1)

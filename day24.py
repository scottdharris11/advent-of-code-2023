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
            p = intersection(stone, stones[j], min, max)
            
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
def intersection(stone1: HailStone, stone2: HailStone, min: int, max: int) -> tuple[float]:
    start1 = stone1.yIntercept(min)
    end1 = stone1.yIntercept(max)
    start2 = stone2.yIntercept(min)
    end2 = stone2.yIntercept(max)
    
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

from utilities.data import read_lines, parse_integers
from utilities.runner import Runner

@Runner("Day 22", "Part 1")
def solve_part1(lines: list):
    world = World(lines)
    world.drop_bricks()
    return len(world.disintegrable_bricks)

@Runner("Day 22", "Part 2")
def solve_part2(lines: list):
    world = World(lines)
    world.drop_bricks()
    impact = 0
    for i in range(len(world.bricks)):
        if i in world.disintegrable_bricks:
            continue
        impacted = set()
        impacted.add(i)
        world.disintegrate_impact(i, impacted)
        impact += len(impacted) - 1
    return impact

class Brick:
    def __init__(self, line: str) -> None:
        start = parse_integers(line.split("~")[0], ",")
        end = parse_integers(line.split("~")[1], ",")
        self.minX = min(start[0], end[0])
        self.maxX = max(start[0], end[0])
        self.minY = min(start[1], end[1])
        self.maxY = max(start[1], end[1])
        self.minZ = min(start[2], end[2])
        self.maxZ = max(start[2], end[2])
    
    def __lt__(self, other) -> bool:
        return self.minZ > other.minZ
    
    def __repr__(self) -> str:
        return str(((self.minX, self.maxX), (self.minY, self.maxY), (self.minZ, self.maxZ)))
    
class World:
    def __init__(self, lines: list[str]) -> None:
        self.bricks = [Brick(line) for line in lines]
        self.bricks.sort()
    
    def __repr__(self) -> str:
        out = ""
        for brick in self.bricks:
            out += str(brick) + "\n"
        return out
    
    def drop_bricks(self) -> None:
        # cycle until all bricks are dropped
        cycle = 1
        while True:
            moved = False
            for i in range(len(self.bricks)-1, -1, -1):
                if self.__drop_brick(i, self.bricks[i]):
                    moved = True
            self.bricks.sort()
            if not moved:
                break
            cycle += 1
        
        # create maps of brick support
        self.supporting = {}
        self.supported_by = {}
        for i in range(len(self.bricks)-1, -1, -1):
            for j in range(len(self.bricks)-1, -1, -1):
                if i == j:
                    continue
                if self.__is_supporting(self.bricks[i], self.bricks[j]):
                    s = self.supporting.get(i, [])
                    s.append(j)
                    self.supporting[i] = s
                    s = self.supported_by.get(j, [])
                    s.append(i)
                    self.supported_by[j] = s
        
        # determine bricks that can be disintegrated
        self.disintegrable_bricks = []
        for i in range(len(self.bricks)):
            if i not in self.supporting:
                self.disintegrable_bricks.append(i)
                continue
            d = True
            for b in self.supporting[i]:
                if len(self.supported_by[b]) == 1:
                    d = False
                    break
            if d:
                self.disintegrable_bricks.append(i)
    
    def disintegrate_impact(self, b: int, bricks: set[int]) -> None:
        if b not in self.supporting:
            return
        newimpact = []
        for sb in self.supporting[b]:
            if sb in bricks:
                continue
            sby = self.supported_by[sb][:]
            for i in sby[:]:
                if i in bricks:
                    sby.remove(i)
            if len(sby) == 0:
                bricks.add(sb)
                newimpact.append(sb)
        for sb in newimpact:
            self.disintegrate_impact(sb, bricks)
    
    def __drop_brick(self, idx: int, brick: Brick) -> bool:
        moved = False
        blocked = False
        while brick.minZ > 1 and not blocked:
            brick.minZ -= 1
            brick.maxZ -= 1
            for i in range(idx+1,len(self.bricks)):
                if brick.maxZ < self.bricks[i].minZ or brick.minZ > self.bricks[i].maxZ:
                    continue
                if self.__overlap(brick, self.bricks[i]):
                    brick.minZ += 1
                    brick.maxZ += 1
                    blocked = True
                    break
            if not blocked:
                moved = True
        return moved
    
    def __overlap(self, b1: Brick, b2: Brick) -> bool:
        if b1.maxZ < b2.minZ or b1.minZ > b2.maxZ:
            return False
        xoverlap = not(b1.maxX < b2.minX or b1.minX > b2.maxX)
        yoverlap = not(b1.maxY < b2.minY or b1.minY > b2.maxY)
        return xoverlap and yoverlap
    
    def __is_supporting(self, b1: Brick, b2: Brick) -> bool:
        if b1.maxZ < b2.minZ - 1 or b2.maxZ < b1.minZ:
            return False
        b2.minZ -= 1
        b2.maxZ -= 1
        s = self.__overlap(b1, b2)
        b2.minZ += 1
        b2.maxZ += 1
        return s
    
# Part 1
input = read_lines("input/day22/input.txt")
sample = read_lines("input/day22/sample.txt")

value = solve_part1(sample)
assert(value == 5)
value = solve_part1(input)
assert(value == 428)

# Part 2
value = solve_part2(sample)
assert(value == 7)
value = solve_part2(input)
assert(value == 35654)

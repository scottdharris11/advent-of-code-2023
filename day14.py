from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 14", "Part 1")
def solve_part1(lines: list):
    p = Platform(lines)
    p.tilt_north()
    return p.load()

@Runner("Day 14", "Part 2")
def solve_part2(lines: list):
    p = Platform(lines)
    
    # find repeat spot
    cyclesToRepeat = 0
    while not p.cycle():
        cyclesToRepeat += 1
    
    # finish cycle and any extras needed
    m = 1000000000 % cyclesToRepeat
    for _ in range(cyclesToRepeat-1+m):
        p.cycle()
    
    return p.load()

class Platform:
    def __init__(self, lines) -> None:
        self.rows = []
        for line in lines:
            self.rows.append(list(line))
        self.row_count = len(self.rows)
        self.col_count = len(self.rows[0])
        self.cyclecache = {}
        self.cachehits = 0
        
    def __repr__(self) -> str:
        output = ""
        for row in self.rows:
            output += "".join(row) + "\n"
        return output
    
    def cycle(self) -> bool:
        h = self.__rowhash()
        if h in self.cyclecache:
            self.rows = self.cyclecache[h]
            self.cachehits += 1
            return True
        self.tilt_north()
        self.tilt_west()
        self.tilt_south()
        self.tilt_east()
        self.cyclecache[h] = self.__copy()
        return False
            
    def tilt_north(self) -> None:
        for i in range(self.col_count):
            block = -1
            for j in range(self.row_count):
                if self.rows[j][i] == '#':
                    block = j
                elif self.rows[j][i] == 'O':
                    if block + 1 < j:
                        self.rows[block+1][i] = 'O'
                        self.rows[j][i] = '.'
                    block += 1
    
    def tilt_west(self) -> None:
        for i in range(self.row_count):
            block = -1
            for j in range(self.col_count):
                if self.rows[i][j] == '#':
                    block = j
                elif self.rows[i][j] == 'O':
                    if block + 1 < j:
                        self.rows[i][block + 1] = 'O'
                        self.rows[i][j] = '.'
                    block += 1
    
    def tilt_south(self) -> None:
        for i in range(self.col_count):
            block = self.row_count
            for j in range(self.row_count-1, -1, -1):
                if self.rows[j][i] == '#':
                    block = j
                elif self.rows[j][i] == 'O':
                    if block - 1 > j:
                        self.rows[block-1][i] = 'O'
                        self.rows[j][i] = '.'
                    block -= 1
    
    def tilt_east(self) -> None:
        for i in range(self.row_count):
            block = self.col_count
            for j in range(self.col_count-1, -1, -1):
                if self.rows[i][j] == '#':
                    block = j
                elif self.rows[i][j] == 'O':
                    if block - 1 > j:
                        self.rows[i][block-1] = 'O'
                        self.rows[i][j] = '.'
                    block -= 1
    
    def load(self) -> int:
        total = 0
        for i, row in enumerate(self.rows):
            l = self.row_count - i
            total += l * row.count("O")
        return total
    
    def __rowhash(self) -> int:
        output = ""
        for row in self.rows:
            output += "".join(row)
        return hash(output)
    
    def __copy(self) -> list:
        output = []
        for row in self.rows:
            output.append(row[:])
        return output

# Part 1
input = read_lines("input/day14/input.txt")
sample = read_lines("input/day14/sample.txt")

value = solve_part1(sample)
assert(value == 136)
value = solve_part1(input)
assert(value == 110821)

# Part 2
value = solve_part2(sample)
assert(value == 64)
value = solve_part2(input)
assert(value == 83516)

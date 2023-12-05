from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 2", "Part 1")
def solve_part1(lines: list):
    actual = {"red":12, "green": 13, "blue": 14}
    total = 0
    for line in lines:
        game = parse_game(line)
        if game.possible(actual):
            total += game.id
    return total

@Runner("Day 2", "Part 2")
def solve_part2(lines: list):
    total = 0
    for line in lines:
        game = parse_game(line)
        total += game.power()
    return total

def parse_game(line: str):
    start = line.index(" ")
    end = line.index(":")
    id = int(line[start+1:end])
    game = Game(id)
    
    sets = line[end+1:].split(";")
    for set in sets:
        cubes = set.split(",")
        for cube in cubes:
            c = cube.strip().split(" ")
            game.show(c[1], int(c[0]))
    
    return game
    
class Game:
    def __init__(self, id) -> None:
        self.id = id
        self.max_cubes = {}
    
    def show(self, color, count):
        if self.max_cubes.get(color, 0) < count:
            self.max_cubes[color] = count
    
    def possible(self, cubes: dict):
        for cube in cubes.keys():
            if self.max_cubes[cube] > cubes[cube]:
                return False
        return True
    
    def power(self):
        p = 1
        for cube in self.max_cubes:
            p *= self.max_cubes[cube]
        return p
    
# Part 1
input = read_lines("input/day2-input.txt")
sample = [
    "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
    "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
    "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
    "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
    "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
]

value = solve_part1(sample)
assert(value == 8)
value = solve_part1(input)
assert(value == 2795)

# Part 2
value = solve_part2(sample)
assert(value == 2286)
value = solve_part2(input)
assert(value == 75561)

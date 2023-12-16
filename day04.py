from utilities.data import read_lines, parse_integers
from utilities.runner import Runner

@Runner("Day 4", "Part 1")
def solve_part1(lines: list):
    total = 0
    for line in lines:
        card = parse_card(line)
        total += card.points()
    return total

@Runner("Day 4", "Part 2")
def solve_part2(lines: list):
    cards = []
    counts = []
    for line in lines:
        cards.append(parse_card(line))
        counts.append(1)
        
    for card in cards:
        for i in card.copies_won():
            counts[i-1] += 1 * counts[card.id-1]
    
    return sum(counts)

def parse_card(line: str):
    c = line.split(":")
    card = Card(int(c[0][5:].strip()))
    n = c[1].split("|")
    card.winning = set(parse_integers(n[0].strip(), " "))
    card.actual = set(parse_integers(n[1].strip(), " "))
    return card

class Card:
    def __init__(self, id) -> None:
        self.id = id
        self.winning = set()
        self.actual = set()
    
    def matches(self):
        return len(self.winning & self.actual)
        
    def points(self):
        m = self.matches()
        if m < 2:
            return m
        return 2**(m-1)
    
    def copies_won(self):
        m = self.matches()
        if m == 0:
            return []
        else:
            return range(self.id+1, self.id+1+m)

# Part 1
input = read_lines("input/day04/input.txt")
sample = [
    "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
    "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
    "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
    "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
    "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
    "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
]

value = solve_part1(sample)
assert(value == 13)
value = solve_part1(input)
assert(value == 22488)

# Part 2
value = solve_part2(sample)
assert(value == 30)
value = solve_part2(input)
assert(value == 7013204)

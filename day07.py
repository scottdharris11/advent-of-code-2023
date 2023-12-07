from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 7", "Part 1")
def solve_part1(lines: list):
    hands = parse_hands(lines)
    hands = sort_hands(hands)
    total = 0
    for i in range(len(hands)):
        total += (i+1) * hands[i].bid
    return total

@Runner("Day 7", "Part 2")
def solve_part2(lines: list):
    return -1

FIVE_OF_KIND = 6
FOUR_OF_KIND = 5
FULL_HOUSE = 4
THREE_OF_KIND = 3
TWO_PAIRS = 2
ONE_PAIR = 1
HIGH_CARD = 0
CARDS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

class Hand:
    def __init__(self, cards, bid) -> None:
        self.cards = cards
        self.bid = bid
        self.type = self.__hand_type()
        
    def __repr__(self): 
        return str((self.cards, self.bid)) 
    
    def compare(self, obj) -> int: 
        if self.type == obj.type:
            for i in range(len(self.cards)):
                if self.cards[i] == obj.cards[i]:
                    continue
                return CARDS.index(self.cards[i]) - CARDS.index(obj.cards[i])
        else:
            return self.type - obj.type
        return 0
        
    def __hand_type(self) -> int:
        counts = {}
        for c in self.cards:
            counts[c] = counts.get(c, 0) + 1
        pairs = 0
        three = False
        for c in counts.values():
            if c == 5:
                return FIVE_OF_KIND
            elif c == 4:
                return FOUR_OF_KIND
            elif c == 3:
                three = True
            elif c == 2:
                pairs += 1
        if three:
            if pairs == 1:
                return FULL_HOUSE
            return THREE_OF_KIND
        elif pairs > 0:
            if pairs > 1:
                return TWO_PAIRS
            return ONE_PAIR
        return HIGH_CARD

def parse_hands(lines: list) -> list[Hand]:
    hands = []
    for line in lines:
        cards, bid = line.split()
        hands.append(Hand(cards, int(bid)))
    return hands

def sort_hands(hands: list[Hand]) -> list[Hand]:
    for i in range(len(hands)-1):
        swapped = False;
        for j in range(len(hands)-i-1):
            a = hands[j]
            b = hands[j+1]
            if a.compare(b) > 0:
                hands[j] = b
                hands[j+1] = a
                swapped = True
        if not swapped:
            break
    return hands

# Part 1
input = read_lines("input/day7-input.txt")
sample = read_lines("input/day7-sample.txt")

value = solve_part1(sample)
assert(value == 6440)
value = solve_part1(input)
assert(value == 247823654)

# Part 2
value = solve_part2(sample)
assert(value == -1)
value = solve_part2(input)
assert(value == -1)

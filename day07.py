from utilities.data import read_lines
from utilities.runner import Runner

@Runner("Day 7", "Part 1")
def solve_part1(lines: list):
    return winnings(parse_hands(lines, False))

@Runner("Day 7", "Part 2")
def solve_part2(lines: list):
    return winnings(parse_hands(lines, True))

FIVE_OF_KIND = 6
FOUR_OF_KIND = 5
FULL_HOUSE = 4
THREE_OF_KIND = 3
TWO_PAIRS = 2
ONE_PAIR = 1
HIGH_CARD = 0
CARDS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

class Hand:
    def __init__(self, cards: str, bid: int, wild: bool) -> None:
        self.cards = cards
        self.bid = bid
        self.wild = wild
        self.type = self.__hand_type(cards)
        
    def __repr__(self): 
        return str((self.cards, self.bid)) 
    
    def compare(self, obj) -> int: 
        if self.type == obj.type:
            for i in range(len(self.cards)):
                if self.cards[i] == obj.cards[i]:
                    continue
                return self.__card_value(self.cards[i]) - self.__card_value(obj.cards[i])
        else:
            return self.type - obj.type
        return 0
    
    def __card_value(self, card: chr) -> int:
        v = CARDS.index(card)
        if self.wild:
            if card == 'J':
                v = 0
            else:
                v += 1
        return v
    
    def __hand_type(self, cards: str) -> int:
        # recursive function to replace Joker with each card type
        # to determine the best type possible
        if self.wild and cards.count('J') > 0:
            if cards.count('J') > 3:
                return FIVE_OF_KIND
            best_type = 0
            for r in CARDS:
                if r == 'J':
                    continue
                best_type = max(self.__hand_type(cards.replace("J", r, 1)), best_type)
                if best_type == FIVE_OF_KIND:
                    return FIVE_OF_KIND
            return best_type
        
        counts = {}
        for c in cards:
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

def parse_hands(lines: list, wild: bool) -> list[Hand]:
    hands = []
    for line in lines:
        cards, bid = line.split()
        hands.append(Hand(cards, int(bid), wild))
    return hands

def winnings(hands: list[Hand]) -> int:
    hands = sort_hands(hands)
    total = 0
    for i in range(len(hands)):
        total += (i+1) * hands[i].bid
    return total

def sort_hands(hands: list[Hand]) -> list[Hand]:
    # simple bubble sort implementation
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
assert(value == 5905)
value = solve_part2(input)
assert(value == 245461700)

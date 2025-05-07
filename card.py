import random
from enum import Enum, IntEnum

class Suit(Enum):
    CLUBS = "Clubs"
    DIAMONDS = "Diamonds"
    HEARTS = "Hearts"
    SPADES = "Spades"

class Rank(IntEnum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

class Deck:
    def __init__(self):
        self.cards = []
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(suit, rank))
        self.shuffle()
        self.discard_pile = []

    def shuffle(self):
        random.shuffle(self.cards)
        
class Hand:
    def __init__(self):
        self.cards = []
        self.total = 0
        self.is_busted = False
        self.is_blackjack = False
        self.is_standing = False
        self.surrendered = False

    def calc_total(self):
        total = 0
        for card in self.cards:
            if card.rank.value >= 10:
                total += 10
            elif 1 < card.rank < 10:
                total += card.rank
        for card in self.cards:
            if card.rank == Rank.ACE:
                if total + 11 <= 21:
                    total += 11
                else:
                    total += 1
        if total > 21:
            self.is_busted = True
        return total

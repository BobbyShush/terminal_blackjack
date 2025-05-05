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

    def shuffle(self):
        random.shuffle(self.cards)
        
class Hand:
    def __init__(self):
        self.cards = []
        self.total = 0

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
        return total

class Dealer(Hand):
    def __init__(self):
        super().__init__()
        self.deck = Deck()

    def initial_deal(self, players):
        self.draw_card()
        self.total = self.calc_total()
        distribute_cards(players, 2)
        for player in players:
            player.total = player.calc_total()

    def draw_card(self):
        self.cards.append(self.deck.pop())

    def distribute_cards(self, players, n):
        for i in range(n):
            for player in players:
                player.cards.append(self.deck.pop())


import unittest

from card import *
from dealer import Dealer
from player import Player
from statemachine import StateMachine

class Tests(unittest.TestCase):
    def test_hand_calc(self):
        # Test 1 - numeral cards
        hand = Hand()
        hand.cards.append(Card(Suit.CLUBS, Rank.TWO))
        hand.cards.append(Card(Suit.CLUBS, Rank.THREE))
        self.assertEqual(5, hand.calc_total())

        # Test 2 - face card
        hand = Hand()
        hand.cards.append(Card(Suit.CLUBS, Rank.TWO))
        hand.cards.append(Card(Suit.CLUBS, Rank.JACK))
        self.assertEqual(12, hand.calc_total())

        # Test 3 - blackjack
        hand = Hand()
        hand.cards.append(Card(Suit.CLUBS, Rank.ACE))
        hand.cards.append(Card(Suit.CLUBS, Rank.QUEEN))
        self.assertEqual(21, hand.calc_total())

        # Test 4 - ace and numeral
        hand = Hand()
        hand.cards.append(Card(Suit.CLUBS, Rank.ACE))
        hand.cards.append(Card(Suit.CLUBS, Rank.THREE))
        self.assertEqual(14, hand.calc_total())

        # Test 4 - ace don't bust
        hand = Hand()
        hand.cards.append(Card(Suit.CLUBS, Rank.KING))
        hand.cards.append(Card(Suit.CLUBS, Rank.THREE))
        hand.cards.append(Card(Suit.CLUBS, Rank.ACE))
        self.assertEqual(14, hand.calc_total())


def visual_test_deck_generation():
    deck = Deck()
    for card in deck.cards:
        print(f"{card.rank.name} of {card.suit.name}")

def visual_test_initial_deal():
    dealer = Dealer()
    players = [Player(0), Player(0), Player(0)]
    dealer.initial_deal(players)
    print(f"Dealer has a {dealer.hand.cards[0].rank.name} of {dealer.hand.cards[0].suit.name}")
    for i, player in enumerate(players):
        print(f"PLAYER {i+1}: {player.hand.total}")
        for card in player.hand.cards:
            print(f"{card.rank.name} of {card.suit.name}")
        if player.hand.is_blackjack:
            print("BLACKJACK!!")

def visual_input_test():
    s = input('This will be printed: ')
    print(s)

def visual_test_intro():
    sm = StateMachine()
    sm.introduction()

def run_visual_tests():
    # visual_test_deck_generation()
    # visual_test_initial_deal()
    # visual_input_test()
    visual_test_intro()
    return

if __name__ == "__main__":
    run_visual_tests()
    unittest.main()
from card import Hand, Deck

class Dealer:
    def __init__(self):
        self.hand = Hand()
        self.deck = Deck()

    def initial_deal(self, players):
        self.draw_card(self)
        self.distribute_cards(players, 2)
        for player in players:
            if player.hand.total == 21:
                player.hand.is_blackjack = True

    def draw_card(self, target):
        target.hand.cards.append(self.deck.cards.pop())
        target.hand.total = target.hand.calc_total()

    def distribute_cards(self, players, n):
        for i in range(n):
            for player in players:
                self.draw_card(player)

    def resolve_hand(self):
        self.draw_card(self)
        if self.hand.total == 21:
            self.hand.is_blackjack = True
            return
        while self.hand.calc_total() < 17:
            self.draw_card(self)
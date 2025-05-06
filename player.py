from card import Hand

class Player:
    def __init__(self, coins):
        self.hand = Hand()
        self.hand2 = None
        self.coins = coins
        self.bet = 0
    
    def set_bet(self, bet):
        if 0 < bet <= self.coins:
            self.bet = bet
            return True
        return False

    def hit(self, dealer, hand):
        hand.cards.append(dealer.deck.cards.pop())
        hand.total = hand.calc_total()
    
    def double_down(self, dealer, hand):
        if self.set_bet(self.bet * 2):
            self.hit(dealer, hand)
            return True
        return False

    def split(self, dealer):
        if self.set_bet(self.bet * 2):
            self.hand2 = Hand()
            self.hand2.cards.append(self.hand.cards.pop())
            self.hit(dealer, self.hand)
            if self.hand.total == 21:
                self.hand.is_blackjack = True
            self.hit(dealer, self.hand2)
            if self.hand2.total == 21:
                self.hand2.is_blackjack = True
            return True
        return False

    def surrender(self):
        self.set_bet(self.bet // 2)
        self.hand.surrendered = True
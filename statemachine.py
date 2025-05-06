import time

from dealer import Dealer
from player import Player
from card import Suit, Rank

class StateMachine:
    def __init__(self):
        self.dealer = Dealer()
        self.players = []

    def introduction(self):
        with open('introduction.txt', encoding="utf-8") as f:
            intro = f.read()
        print(intro)
        ready = input("IF YOU ARE READY TO PLAY PRESS ENTER")
        self.player_inscription()

    def player_inscription(self):
        #For now, might implement multiplayer later
        self.players.append(Player(100))
        print("\nGame initiated with 1 player\n")
        time.sleep(1)
        print("BETS")
        print("****************************************\n")
        self.place_bets()

    def place_bets(self):
        for i, player in enumerate(self.players):
            time.sleep(1)
            print(f"PLAYER{i+1}, PLACE YOUR BET")
            print(f"You currently have {player.coins} coins")
            bet = ""
            while bet == "":
                bet = input("BET = ")
                if bet.isdigit():
                    if not player.set_bet(int(bet)):
                        print("You cannot bet that!")
                        bet = ""
                        continue
                    player.set_bet(int(bet))
                    print(f"BET REGISTERED: {player.bet}\n")
                else:
                    print("You cannot bet that!")
                    bet = ""

        time.sleep(1)
        print("INITIAL DEAL")
        print("****************************************\n")
        self.initial_deal()

    def initial_deal(self):
        self.dealer.initial_deal(self.players)
        print(f"DEALER'S CARD: {self.dealer.hand.cards[0].rank.name} of {self.dealer.hand.cards[0].suit.name}")
        print(f"DEALER'S CURRENT SCORE: {self.dealer.hand.total}")
        print("****************************************\n")
        for i, player in enumerate(self.players):
            time.sleep(1)
            print(f"PLAYER{i+1}'s TURN\n")
            time.sleep(1)
            self.player_turn(player, player.hand)
            print("****************************************\n")

        # Dealer's resolve
    
    def player_turn(self, player, hand, first_action=True):
        if (
            hand.is_blackjack or
            hand.is_busted or
            hand.is_standing or
            hand.surrendered
        ):
            return
        print("YOUR CARDS ARE:")
        ace_count = 0
        for card in hand.cards:
            if card.rank == Rank.ACE:
                ace_count += 1
            print(f"{card.rank.name} of {card.suit.name}")
        print(f"YOUR CURRENT SCORE IS: {hand.total}")
        time.sleep(1)

        if hand.is_blackjack:
            print("YOU HAVE A BLACKJACK! TAKE IT EASY!")
            return

        if first_action:
            if ace_count == 2 and player.bet * 2 < player.coins:
                self.print_menu(player, 'splitmenu.txt', hand)
                return

            if player.bet * 2 < player.coins:
                self.print_menu(player, 'doubledownmenu.txt', hand)
                return

        self.print_menu(player, 'hitmenu.txt', hand)

    def print_menu(self, player, menu, hand):
        with open(menu, encoding="utf-8") as f:
            menu_str = f.read()
        print(menu_str)
        action = ""
        while action == "":
            action = input("Enter the action number for your choice, then press ENTER: ")
            if ((action == "5" and menu != 'splitmenu.txt') or 
            ((action == "4" or action == "3") and menu != 'doubledownmenu.txt') or
            (action not in ['1', '2', '3', '4', '5'])
            ):
                print("Invalid entry. Try again. Example: '1'")
                action = ""
        self.menu_action(player, action, hand)
    
    def menu_action(self, player, action, hand):
        match action:
            case "1": # HIT
                player.hit(self.dealer, hand)
                self.hit_followup(hand)
                self.player_turn(player, hand, False)
            case "2": # STAND
                hand.is_standing = True
            case "3": # DOUBLE DOWN
                player.double_down(self.dealer, hand)
                time.sleep(1)
                print(f"\nYour total bet is now {player.bet}")
                self.hit_followup(hand)
                self.player_turn(player, hand, False)
            case "4": # SURRENDER
                player.surrender()
                time.sleep(1)
                print(f"\nYour total bet is now {player.bet}")
            case "5": # SPLIT
                player.split(self.dealer)
                time.sleep(1)
                print("\nYou now have TWO HANDS")
                print("They will be played ONE BY ONE")

                time.sleep(1)
                print("****************************************\n")
                print("HAND ONE")
                self.player_turn(player, player.hand, False)

                time.sleep(1)
                print("****************************************\n")
                print("HAND TWO")
                self.player_turn(player, player.hand2, False)

    def hit_followup(self, hand):
        print(f"\nYOU DRAW A {hand.cards[-1].rank.name} of {hand.cards[-1].suit.name}")
        print(f"THIS HAND'S NEW SCORE IS: {hand.total}\n")
        if hand.total > 21:
            time.sleep(1)
            print("BUSTED!\n")
            hand.is_busted = True
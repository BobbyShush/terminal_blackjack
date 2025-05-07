import time

from dealer import Dealer
from player import Player
from card import Suit, Rank

MINIMUM_BET = 10

class StateMachine:
    def __init__(self):
        self.dealer = Dealer()
        self.players = [] # for future multi-player handling

    # Displays the game's rules
    def introduction(self):
        with open('introduction.txt', encoding="utf-8") as f:
            intro = f.read()
        print(intro)
        ready = input("IF YOU ARE READY TO PLAY PRESS ENTER")

        # To the next step
        self.player_inscription()

    # Initiate the players
    def player_inscription(self):
        #For now, single player only, might implement multiplayer later
        self.players.append(Player(100))
        print("\nGame initiated with 1 player\n")

        # To the next step
        time.sleep(1)
        print("BETS")
        print("****************************************\n")
        self.place_bets()

    # Handle player bets
    def place_bets(self):
        print(f"MINIMUM BET: {MINIMUM_BET} COINS")
        for i, player in enumerate(self.players):
            time.sleep(1)
            print(f"PLAYER{i+1}, PLACE YOUR BET")
            print(f"You currently have {player.coins} coins")

            # Handle player with insufficient coins
            if player.coins < MINIMUM_BET:
                print("YOU DON'T HAVE ENOUGH COINS!")
                answer = ""
                while answer == "":
                    answer = input("WANT TO BORROW 100 COINS FROM THE HOUSE (Y/N): ")
                    if answer.lower() not in ['y', 'n']:
                        print("Invalid entry. Try again.")
                        answer = ""
                if answer.lower() == 'n':
                    exit() # for now, will handle differently if multiplayer
                player.coins += 100
                print(f"You now have {player.coins} coins")

            # Take player input for bet
            bet = ""
            while bet == "":
                bet = input("BET = ")
                if bet.isdigit():
                    bet_amount = int(bet)
                    if bet_amount < MINIMUM_BET:
                        print(f"Bet must be at least {MINIMUM_BET} coins!")
                        bet = ""
                        continue
                    if not player.set_bet(int(bet)):
                        print("You cannot bet that!")
                        bet = ""
                        continue
                    print(f"BET REGISTERED: {player.bet}\n")
                else:
                    print("You cannot bet that!")
                    bet = ""

        # To the next step
        time.sleep(1)
        print("INITIAL DEAL")
        print("****************************************\n")
        self.round()

    # From the player turns to the end of the round
    def round(self):
        # Dealer shows his card
        self.dealer.initial_deal(self.players)
        print(f"DEALER'S CARD: {self.dealer.hand.cards[0].rank.name} of {self.dealer.hand.cards[0].suit.name}")
        print(f"DEALER'S CURRENT SCORE: {self.dealer.hand.total}")
        print("****************************************\n")

        # Player turns
        for i, player in enumerate(self.players):
            time.sleep(1)
            print(f"PLAYER{i+1}'s TURN\n")
            time.sleep(1)
            self.player_turn(player, player.hand)
            print("****************************************\n")

        # Dealer's turn and player evaluation
        time.sleep(1)
        print("DEALER'S TURN")
        print("****************************************\n")
        self.dealer_resolve()

        # Contination message and table reset
        time.sleep(1)
        print("\nEND OF ROUND")
        print("****************************************\n")
        self.end_of_round()
    
    # Hand entry point for a turn
    def player_turn(self, player, hand, first_action=True):
        # Guard statement / Base case
        if (
            hand.is_busted or
            hand.is_standing or
            hand.surrendered
        ):
            return

        # Display the cards and score    
        print("YOUR CARDS ARE:")
        ace_count = 0
        for card in hand.cards:
            if card.rank == Rank.ACE:
                ace_count += 1
            print(f"{card.rank.name} of {card.suit.name}")
        print(f"YOUR CURRENT SCORE IS: {hand.total}")
        time.sleep(1)

        # Handle blackjack and end the turn
        if hand.is_blackjack:
            return print("YOU HAVE A BLACKJACK! TAKE IT EASY!")

        # SPLIT, DOUBLE DOWN and SURRENDER are only displayed on the first action menu
        if first_action:

            # SPLIT is only available if the player starts with two aces, handle player response
            if ace_count == 2 and player.bet * 2 < player.coins:
                return self.print_menu(player, 'menu_split.txt', hand)

            # DOUBLE DOWN and SURRENDER menu display, handle player response
            if player.bet * 2 < player.coins:
                return self.print_menu(player, 'menu_double.txt', hand)

            # SURRENDER menu display, handle player response
            return self.print_menu(player, 'menu_surrender.txt', hand)

        # HIT and STAND menu display (basic options), handle player repsonse
        self.print_menu(player, 'menu_cont.txt', hand)

    # Menu display and input handling
    def print_menu(self, player, menu, hand):
        with open(menu, encoding="utf-8") as f:
            menu_str = f.read()
        print(menu_str)

        action = ""
        while action == "":
            action = input("Enter the action number for your choice, then press ENTER: ")
            if any([
                (action == "5" and menu != 'menu_split.txt'), 
                (action == "4" and all([menu != 'menu_split.txt', menu != 'menu_double.txt'])),
                (action == "3" and all([menu != 'menu_split.txt', menu != 'menu_double.txt', menu != 'menu_surrender.txt'])),
                (action not in ['1', '2', '3', '4', '5']),
            ]):
                print("Invalid entry. Try again. Example: '1'")
                action = ""

        # Next step based on player input
        self.menu_action(player, action, hand)
    
    def menu_action(self, player, action, hand):
        match action:
            # HIT draws card, displays updated score and reenters a turn for the same hand
            case "1": 
                player.hit(self.dealer, hand)
                self.hit_followup(hand)
                self.player_turn(player, hand, False)

            # STAND sets the standing flag and ends the turn
            case "2": 
                hand.is_standing = True

            # SURRENDER sets the surrendered flag, updates/displays the bet and ends the turn
            case "3": 
                player.surrender()
                time.sleep(1)
                print(f"\nYour total bet is now {player.bet}")                

            # DOUBLE DOWN doubles bet, draws card, displays updated score and reenters a turn (only 1 hand)
            case "4":
                player.double_down(self.dealer, hand)
                time.sleep(1)
                print(f"\nYour total bet is now {player.bet}")
                self.hit_followup(hand)
                self.player_turn(player, hand, False)

            # SPLIT doubles bet, creates hand2, splits the cards between the hands
            # draws a new card for each hand and enters a new turn for each hand
            # each hand will resolve consecutively by recursion
            case "5": 
                player.split(self.dealer)
                time.sleep(1)
                print(f"\nYour total bet is now {player.bet}")
                print("You now have TWO HANDS")
                print("They will be played ONE BY ONE")

                time.sleep(1)
                print("****************************************\n")
                print("HAND ONE")
                self.player_turn(player, player.hand, False)

                time.sleep(1)
                print("****************************************\n")
                print("HAND TWO")
                self.player_turn(player, player.hand2, False)

    # helper method used on HIT and DOUBLEDOWN to display the drawn card,
    # updated score and possible BUST
    def hit_followup(self, hand):
        print(f"\nYOU DRAW A {hand.cards[-1].rank.name} of {hand.cards[-1].suit.name}")
        print(f"THIS HAND'S NEW SCORE IS: {hand.total}\n")
        if hand.total > 21:
            time.sleep(1)
            print("BUSTED!\n")
            hand.is_busted = True

    # Dealer's turn
    def dealer_resolve(self):
        self.helper_dealer_resolve() # draw a card

        # Handle blackjack
        if self.dealer.hand.total == 21:
            self.dealer.hand.is_blackjack = True
            time.sleep(1)
            print(f"THE DEALER HAS A BLACKJACK! NO LUCK FOR YOU TODAY!")
            return self.evaluate_result() # To next step

        # Keep drawing until score is above eleven
        # Current implementation stops at a soft 17
        # Meaning it doesn't keep hitting even if 17
        # is obtained with an ace (example: ACE + 6)
        while self.dealer.hand.total < 17:
            self.helper_dealer_resolve()

        # Handle bust
        if self.dealer.hand.total > 21:
            self.dealer.hand.is_busted = True
            time.sleep(1)
            print(f"\nTHE DEALER BUSTED! LUCKY!")
            return self.evaluate_result() # To next step

        # To next step
        self.evaluate_result()

    # Draw a card, display it and display the updated score
    def helper_dealer_resolve(self):
        self.dealer.draw_card(self.dealer)
        time.sleep(1)
        print(f"THE DEALER DRAWS A {self.dealer.hand.cards[-1].rank.name} of {self.dealer.hand.cards[-1].suit.name}")
        print(f"THE DEALER'S CURRENT SCORE IS: {self.dealer.hand.total}\n")

    # Wrapper evaluate method to display results per player
    # Once the results are evaluated, the code returns all the
    # way back to the self.round() method
    def evaluate_result(self):
        for i, player in enumerate(self.players):
            time.sleep(1)
            print(f"\nPLAYER{i+1}'S RESULT:")
            self.evaluate_player(player, self.dealer)

    # Base of the decision tree
    def evaluate_player(self, player, dealer):
        if player.hand.surrendered:
            return self.handle_surrender(player)

        if dealer.hand.is_blackjack:
            return self.handle_dealer_blackjack(player)

        if dealer.hand.is_busted:
            return self.handle_dealer_bust(player)

        if player.hand2:
            return self.handle_split_hand(player, dealer)

        return self.handle_normal_comparison(player, dealer)
        
    # Possible results
    def standoff(self):
        print("STANDOFF: Nothing happens")

    def lose(self, player):
        print(f"YOU LOSE {player.bet} COINS")
        player.coins -= player.bet

    def win(self, player):
        print(f"YOU WIN {player.bet} COINS")
        player.coins += player.bet

    # Situational handlers        
    def handle_surrender(self, player):
        print(f"COWARD! YOU LOSE {player.bet}")
        player.coins -= player.bet

    def handle_dealer_blackjack(self, player):
        if player.hand2:
            if any([player.hand.is_blackjack, player.hand2.is_blackjack]):
                self.standoff()
            else:
                self.lose(player)
        elif player.hand.is_blackjack:
            self.standoff()
        else:
            self.lose(player)

    def handle_dealer_bust(self, player):
        if player.hand2:
            if not all([player.hand.is_busted, player.hand2.is_busted]):
                self.win(player)
            else:
                self.lose(player)
        elif not player.hand.is_busted:
            self.win(player)
        else:
            self.lose(player)

    def handle_split_hand(self, player, dealer):
        if any([
            player.hand.is_blackjack, 
            player.hand2.is_blackjack,
            (player.hand.total > dealer.hand.total and not player.hand.is_busted),
            (player.hand2.total > dealer.hand.total and not player.hand.is_busted),
        ]):
            self.win(player)
        elif any([
            player.hand.total == dealer.hand.total,
            player.hand2.total == dealer.hand2.total,
        ]):
            self.standoff()
        else:
            self.lose(player)

    def handle_normal_comparison(self, player, dealer):
        if any([
            player.hand.is_blackjack,
            (player.hand.total > dealer.hand.total and not player.hand.is_busted),
        ]):
            self.win(player)
        elif player.hand.total == dealer.hand.total:
            self.standoff()
        else:
            self.lose(player)

    # Player continue decision handling and table reset
    # Circles back to the bets phase
    def end_of_round(self):
        answer = ""
        while answer == "":
            time.sleep(1)
            answer = input("KEEP PLAYING? (Y/N): ")
            if answer.lower() not in ['y', 'n']:
                print("Invalid entry. Try again.")
                answer = ""
        if answer.lower() == 'n':
            exit()
        self.dealer = Dealer()
        for i in range(len(self.players)):
            self.players[i] = Player(self.players[i].coins)
        time.sleep(1)
        print("BETS")
        print("****************************************\n")
        self.place_bets()

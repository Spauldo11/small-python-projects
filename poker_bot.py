import random
buy_in = 20 # placeholder
num_people = 4

class Card:
    def __init__(self, suit, val):
        self.suit = suit
        self.val = val

class Pocket:
    def __init__(self):
        self.cards = []
    def add_card(self, card):
        self.cards.append(card)
    
    # Calculates the strength of your pocket hand alone
    def calc_strength(self):
        card1 = self.cards[0]
        card2 = self.cards[1]
        # Make the alternate values bad initially so the alternate strength won't get selected if there are no aces
        alter_card1 = Card(card1.suit, 0)
        alter_card2 = Card(card2.suit, 0)
        alter_difference = 10000
        alter_joint_val = 0
        alter_pair = 0
        if card1.val == 1:
            alter_card1 = Card(card1.suit, 14)
        if card2.val == 1:
            alter_card2 = Card(card2.suit, 14)
        # Calculates values if the aces were high
        if card1.val == 1 or card2.val == 1:
            alter_difference = abs(alter_card1.val - alter_card2.val)
            alter_joint_val = alter_card1.val + alter_card2.val
            alter_pair = int(alter_difference == 0)
        # The difference in value between the two cards (more is bad)
        difference = abs(card1.val - card2.val)
        # Determines if the two cards are the same suit
        suited = int(card1.suit == card2.suit)
        # Determines the joint value of the two cards
        joint_val = card1.val + card2.val
        # Determines if the two cars make a pair
        pair = int(difference == 0)
        # Determines if a straight is possible given these two cards
        straight_possible = int(0 < difference <= 4)
        # Calculate total strength with aces being low
        total_strength = joint_val*5 + suited*20 + pair*50 - (difference*2 * straight_possible) + straight_possible*20
        # Calculate total strength with aces being high
        alter_strength = alter_joint_val*5 + suited*20 + alter_pair*50 - (alter_difference*2 * straight_possible) + straight_possible*20
        # Return whichever strength is stronger
        if total_strength >= alter_strength:
            return total_strength
        else:
            return alter_strength

class Middle:
    def __init__(self):
        self.cards = []
    def add_card(self, card):
        self.cards.append(card)

class Deck:
    def __init__(self):
        # Represents the four suits of a deck of cards
        self.suits = ["Spades", "Clubs", "Hearts", "Diamonds"]
        self.nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        # Declare deck as 8 decks of cards, similar to casino style poker
        self.cards = [Card(suit, val) for i in range(8) for suit in self.suits for val in self.nums]
        self.shuffle()

    def shuffle(self):
        for i in range(20): # Just to be thourough
            random.shuffle(self.cards)

    def deal_card(self):
        if not self.cards:
            self.__init__() # Reshuffle if deck is empty
        return self.cards.pop()
    
class Round:#
    def __init__(self):
        self.deck = Deck()
        self.hand = Pocket()
        self.middle = Middle()
        self.current_bet = buy_in # To play a round, you must at least bet the buy in
        self.pot = buy_in * num_people
    def raise_bet(self, amount):
        self.current_bet += amount
        self.pot += amount
    def deal(self):
        for i in range(2):
            self.hand.add_card(self.deck.deal_card())
        strength = self.hand.calc_strength()
        print(f"Hand is {self.hand.cards[0].val} of {self.hand.cards[0].suit} and {self.hand.cards[1].val} of {self.hand.cards[1].suit}")
        print(f"Hand strength is {str(strength)} out of 210")
        if strength > 115:
            self.raise_bet(self.current_bet)
            print("Raise 2x the buy in")
        elif strength > 95:
            self.raise_bet(self.current_bet*.5)
            print("Raise 1.5x the buy in")
    class Flop:
        def __init__(self):
            self.hand = Pocket()
            self.deck = Deck()
            self.middle = Middle()
            self.round = Round()
        def deal_flop(self):
            for i in range(3):
                self.middle.add_card(self.deck.deal_card())
            print(f"The flop is a {self.middle.cards[0].val} of {self.middle.cards[0].suit}, a {self.middle.cards[1].val} of {self.middle.cards[1].suit}, and a {self.middle.cards[2].val} of {self.middle.cards[2].suit}")
            self.round.raise_bet(self.round.current_bet*.5)
    class Turn:
        def __init__(self):
            self.hand = Pocket()
            self.deck = Deck()
            self.middle = Middle()
            self.round = Round()
        def deal_turn(self):
            self.middle.add_card(self.deck.deal_card())
    class River:
        def __init__(self):
            self.hand = Pocket()
            self.deck = Deck()
            self.middle = Middle()
            self.round = Round()
        def deal_river(self):
            self.middle.add_card(self.deck.deal_card())

round = Round()
flop = round.Flop()
turn = round.Turn()
river = round.River()
round.deal()
flop.deal_flop()
turn.deal_turn()
river.deal_river()
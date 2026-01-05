import random
buy_in = 20 # placeholder
num_people = 4
all_cards = []

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
        self.all_cards = []
        self.current_bet = buy_in # To play a round, you must at least bet the buy in
        self.pot = buy_in * num_people
    def raise_bet(self, amount):
        self.current_bet += amount
        self.pot += amount
    def deal(self):
        for i in range(2):
            new_card = self.deck.deal_card()
            self.hand.add_card(new_card)
            all_cards.append(new_card)
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
                new_card = self.deck.deal_card()
                self.middle.add_card(new_card)
                all_cards.append(new_card)
            print(f"The flop is a {self.middle.cards[0].val} of {self.middle.cards[0].suit}, a {self.middle.cards[1].val} of {self.middle.cards[1].suit}, and a {self.middle.cards[2].val} of {self.middle.cards[2].suit}")
            self.round.raise_bet(self.round.current_bet*.5)
    class Turn:
        def __init__(self):
            self.hand = Pocket()
            self.deck = Deck()
            self.middle = Middle()
            self.round = Round()
        def deal_turn(self):
            new_card = self.deck.deal_card()
            self.middle.add_card(new_card)
            all_cards.append(new_card)
            print(f"The turn is a {self.middle.cards[0].val} of {self.middle.cards[0].suit}")
    class River:
        def __init__(self):
            self.hand = Pocket()
            self.deck = Deck()
            self.middle = Middle()
            self.round = Round()
        def deal_river(self):
            new_card = self.deck.deal_card()
            self.middle.add_card(new_card)
            all_cards.append(new_card)
            print(f"The turn is a {self.middle.cards[0].val} of {self.middle.cards[0].suit}")

pairs = []
triples = []
flushes = []
straights = []
straight_flushes = []
quartets = []

# TODO create sorting algorithm for card object. Sort by value
def sort_all_cards(arr):
    pass

def binary_search(start, end, arr, target):
    while start <= end:
        mid = start + (end - start) // 2
        if arr[mid] == target:
            return arr[mid]
        elif arr[mid] > target:
            end = mid - 1
        else:
            start = mid + 1

def check_fours(arr):
    index = 0
    while index <= 3:
        count = 0
        for i in range(index+1, len(arr)):
            if arr[i].val == arr[i-1].val:
                count+=1
            else:
                break
            if count == 3:
                if arr[index].val == 1:
                    arr[index].val = 14
                quartets.append(arr[index])
        index+=1
    return len(quartets)

def check_straight(arr):
    index = 0
    while index <= 2:
        count = 0
        for i in range(index+1, len(arr)):
            if arr[i-1].val == 1:
                arr[i-1].val = 14
                arr.sort()
                break
            if arr[i].val - 1 == arr[i-1].val:
                count+=1
            else:
                break
            if count == 4:
                straights.append(arr[index])
                straight_flushes.append(arr[index])
        index+=1
    return len(straights)

def check_flush(arr):
    index = 0
    while index <= 2:
        count = 0
        for i in range(index+1, len(arr)):
            if arr[i].suit == arr[i-1].suit:
                count+=1
            else:
                break
            if count >= 4:
                flushes.append(arr[index])
        index+=1
    return len(flushes)

def check_triple(arr):
    index = 0
    while index <= 4:
        count = 0
        for i in range(index+1, len(arr)):
            if arr[i].val == arr[i-1].val:
                count+=1
            else:
                break
            if count == 2:
                if arr[index].val == 1:
                    arr[index].val = 14
                triples.append(arr[index])
        index+=1
    return len(triples)

def check_pairs(arr):
# Use for loop and nested binary search to search for pairs within the array. O(nlog(n)) time complexity.
    for i in range(len(arr)-1):
        target = arr[i].val
        low = i+1
        high = len(arr)-1
        if not binary_search(low, high, arr, target) == 1:
            pairs.append(binary_search(low, high, arr, target))
        else:
            binary_search(low, high, arr, target).val = 14
            pairs.append(binary_search(low, high, arr, target))
    return len(pairs)

round = Round()
flop = round.Flop()
turn = round.Turn()
river = round.River()
round.deal()
flop.deal_flop()
turn.deal_turn()
river.deal_river()

four_of_kind = check_fours(all_cards)
straight = check_straight(all_cards)
flush = check_flush(all_cards)
three_of_kind = check_triple(all_cards)
doubles = check_pairs(all_cards)

if four_of_kind > 0:
    print(f"The best is a four of a kind of {quartets[four_of_kind-1].val}\'s")
elif straight > 0:
    for i in range(1, 5):
        straights.append(straights[straight-1]+i)
    straight_flush = check_flush(straights)
    if straight_flush > 0:
        print(f"The best is a straight flush from {straights[straight-1].val} to {straights[straight+3].val} of the suit {straight_flushes[0].suit}")
        if straights[straight-1] == 10:
            print(f"Congrats! it\'s a royal flush of the suit {straight_flushes[0].suit}. That is the rarest hand in all of poker!")
    else:
        print(f"The best is a straight from {straights[straight-1].val} to {straights[straight+3].val}")
elif flush > 0:
    print(f"You have a flush of the suit {flushes[0].suit}")
elif three_of_kind > 0:
    print(f"The best is three of a kind of {triples[three_of_kind-1].val}\'s")
elif doubles > 0 and pairs[0]:
    if doubles > 1:
        print(f" The best is two-pair of {pairs[doubles-1].val}\'s and {pairs[doubles-2].val}\'s")
    else:
        print(f"The best is a pair of {pairs[doubles-1].val}\'s", end="")
else:
    print(f"Your best is a high card: {all_cards[len(all_cards)-1].val}")
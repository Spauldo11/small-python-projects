import random
buy_in = 20 # placeholder
current_bet = buy_in
num_people = 4
pot = buy_in*num_people
final_hands = []
def turn_to_str(num):
    match num:
        case 14:
            return "Ace"
        case 1:
            return "Ace"
        case 13:
            return "King"
        case 12:
            return "Queen"
        case 11:
            return "Jack"
        case _:
            return num
# Define all these functions as empty at the start of the program to use before I fully define them
def sort_all_cards(arr):
    if not arr:
        return arr
    arr.sort(key=lambda card: card.val)
    return arr

def binary_search(start, end, arr, target):
    while start <= end:
        mid = start + (end - start) // 2
        if arr[mid].val == target:
            return arr[mid]
        elif arr[mid].val > target:
            end = mid - 1
        else:
            start = mid + 1

def check_fours(arr, quartets):
    index = 0
    while index <= len(arr)-2:
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

def check_straight(arr, straights, straight_flushes):
    index = 0
    while index <= len(arr)-3:
        count = 0
        for i in range(index+1, len(arr)):
            if arr[i-1].val == 1:
                arr[i-1].val = 14
                sort_all_cards(arr)
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

def check_flush(arr, flushes):
    index = 0
    while index <= len(arr)-3:
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

def check_triple(arr, triples):
    index = 0
    while index <= len(arr)-1:
        count = 0
        for i in range(index+1, len(arr)):
            if arr[i].val == arr[i-1].val:
                count+=1
            else:
                count = 0
                break
            if count == 2:
                if arr[index].val == 1:
                    arr[index].val = 14
                triples.append(arr[index])
        index+=1
    return len(triples)

def check_pairs(arr, pairs):
# Use for loop and nested binary search to search for pairs within the array. O(nlog(n)) time complexity.
    for i in range(len(arr)-1):
        target = arr[i].val
        low = i+1
        high = len(arr)-1
        if (not (target == 1)) and binary_search(low, high, arr, target):
            if len(pairs) > 0:
                if pairs[0] == target:
                    pairs.append(binary_search(low, high, arr, target))
                    continue
            else:
                pairs.append(binary_search(low, high, arr, target))
                continue
        elif binary_search(low, high, arr, target):
            binary_search(low, high, arr, target).val = 14
            if len(pairs) > 0:
                if pairs[0] == binary_search(low, high, arr, target):
                    pairs.append(binary_search(low, high, arr, target))
                    continue
            else:
                pairs.append(binary_search(low, high, arr, target))
                continue
    return len(pairs)
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
        alter_card1 = Card(card1.suit, card1.val)
        alter_card2 = Card(card2.suit, card1.val)
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
        total_strength = joint_val*5 + suited*20 + pair*90 - (difference*2 * straight_possible) + straight_possible*20
        # Calculate total strength with aces being high
        alter_strength = alter_joint_val*5 + suited*20 + alter_pair*90 - (alter_difference*2 * straight_possible) + straight_possible*20
        # Return whichever strength is stronger
        if total_strength >= alter_strength:
            return total_strength
        else:
            if card1.val == 1:
                self.cards[0] = alter_card1
            if card2.val == 1:
                self.cards[1] = alter_card2
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
    
class Bot:
    def __init__(self, name):
        self.name = name
        self.hand = Pocket()
        self.all_cards = []
        self.pairs = []
        self.triples = []
        self.flushes = []
        self.straights = []
        self.straight_flushes = []
        self.quartets = []
        self.pot = buy_in * num_people
        self.total_money = 4000-buy_in
        self.final_num = 0
        self.best = ''
    def raise_bet(self, amount):
        global current_bet, pot
        if amount > self.total_money:
            amount = self.total_money
        current_bet += amount
        self.total_money -= amount
        pot += amount
    def calc_strength(self):
        sort_all_cards(self.all_cards)
        four_of_kind = check_fours(self.all_cards, self.quartets)
        straight = check_straight(self.all_cards, self.straights, self.straight_flushes)
        flush = check_flush(self.all_cards, self.flushes)
        three_of_kind = check_triple(self.all_cards, self.triples)
        doubles = check_pairs(self.all_cards, self.pairs)
        self.raise_amount = 0

        if four_of_kind > 0:
            self.raise_amount = current_bet*4
        elif straight > 0:
            for i in range(1, 5):
                self.straights.append(self.straights[straight-1]+i)
            straight_flush = check_flush(self.straights)
            if straight_flush > 0:
                self.raise_bet(current_bet*4)
                if self.straights[straight-1] == 10:
                    self.raise_bet(self.total_money)
            else:
                self.raise_amount = current_bet*3
        elif flush > 0:
            self.raise_amount = current_bet*3
        elif three_of_kind > 0:
            self.raise_amount = current_bet*3
        elif doubles > 0 and doubles>0:
            if doubles > 1:
                self.raise_amount = current_bet*2
            else:
                self.raise_amount = current_bet*0.5
        else:
            # Including a random chance at a bluff
            if random.randint(0,101) > 75:
                self.raise_amount = current_bet*0.5
        print(f'{self.name} is raising ${self.raise_amount}')
        self.raise_bet(self.raise_amount)
    def eval_hand(self):
        strength = self.hand.calc_strength()
        print(f"{self.name}\'s hand is {turn_to_str(self.hand.cards[0].val)} of {self.hand.cards[0].suit} and {turn_to_str(self.hand.cards[1].val)} of {self.hand.cards[1].suit}")
        # print(f"{self.name}\'s hand strength is {str(strength)} out of 210")
        if strength > 115:
            self.raise_bet(current_bet)
            print(f"{self.name} raises 2x the buy in")
        elif strength > 95:
            self.raise_bet(current_bet*.5)
            print(f"{self.name} raises 1.5x the buy in")
    def end_game(self):
        sort_all_cards(self.all_cards)
        four_of_kind = check_fours(self.all_cards, self.quartets)
        straight = check_straight(self.all_cards, self.straights, self.straight_flushes)
        flush = check_flush(self.all_cards, self.flushes)
        three_of_kind = check_triple(self.all_cards, self.triples)
        doubles = check_pairs(self.all_cards, self.pairs)

        if four_of_kind > 0:
            print(f"The best {self.name} has is a four of a kind of {turn_to_str(self.quartets[four_of_kind-1].val)}\'s")
            self.final_num = 8
            self.best = f"four of a kind of {turn_to_str(self.quartets[four_of_kind-1].val)}\'s"
        elif flush > 0:
            for i in range(1, 5):
                self.flushes.append(self.flushes[flush-1]+i)
            straight_flush = check_straight(self.flushes)
            if straight_flush > 0:
                print(f"The best {self.name} has is a straight flush from {turn_to_str(self.straights[straight-1].val)} to {turn_to_str(self.straights[straight+3].val)} of the suit {turn_to_str(self.straight_flushes[0].suit)}")
                self.final_num = 9
                self.best = f"straight flush from {turn_to_str(self.straights[straight-1].val)} to {turn_to_str(self.straights[straight+3].val)} of the suit {turn_to_str(self.straight_flushes[0].suit)}"
                if self.straights[straight-1] == 10:
                    print(f"Congrats! {self.name} has a royal flush of the suit {turn_to_str(self.straight_flushes[0].suit)}. That is the rarest hand in all of poker!")
                    self.final_num = 10
                    self.best = f"royal flush of the suit {turn_to_str(self.straight_flushes[0].suit)}. That is the rarest hand in all of poker!"
            else:
                print(f"The best {self.name} has is a flush of the suit {turn_to_str(self.flushes[0].suit)}")
                self.final_num = 6
                self.best = f"flush of the suit {turn_to_str(self.flushes[0].suit)}"
        elif straight > 0:
            print(f"The best {self.name} has is a straight from {turn_to_str(self.straights[straight-1].val)} to {turn_to_str(self.straights[straight+3].val)}")
            self.final_num = 5
            self.best = f"straight from {turn_to_str(self.straights[straight-1].val)} to {turn_to_str(self.straights[straight+3].val)}"
        elif three_of_kind > 0:
            if doubles > 0:
                print(f"The best {self.name} has is a full house of {turn_to_str(self.triples[three_of_kind-1].val)} and {turn_to_str(self.pairs[doubles-1].val)}")
                self.final_num = 7
                self.best = f"full house of {turn_to_str(self.triples[three_of_kind-1].val)} and {turn_to_str(self.pairs[doubles-1].val)}"
            print(f"The best {self.name} has is a three of a kind of {turn_to_str(self.triples[three_of_kind-1].val)}\'s")
            self.final_num = 4
            self.best = f"three of a kind of {turn_to_str(self.triples[three_of_kind-1].val)}\'s"
        elif doubles > 0:
            if doubles > 1:
                print(f"The best {self.name} has is a two-pair of {turn_to_str(self.pairs[doubles-1].val)}\'s and {turn_to_str(self.pairs[doubles-2].val)}\'s")
                self.final_num = 3
                self.best = f"two-pair of {turn_to_str(self.pairs[doubles-1].val)}\'s and {turn_to_str(self.pairs[doubles-2].val)}\'s"
            else:
                print(f"The best {self.name} has is a pair of {turn_to_str(self.pairs[doubles-1].val)}\'s")
                self.final_num = 2
                self.best = f"pair of {turn_to_str(self.pairs[doubles-1].val)}\'s"
        else:
            print(f"The best {self.name} has is a high card: {turn_to_str(self.all_cards[len(self.all_cards)-1].val)}")
            self.final_num = 1
            self.best = f"high card: {turn_to_str(self.all_cards[len(self.all_cards)-1].val)}"
        final_hands.append(self)
    
class Round:
    def __init__(self):
        self.deck = Deck()
        self.middle = Middle()
        self.bot1 = Bot("Bot 1")
        self.bot2 = Bot("Bot 2")
        self.bot3 = Bot("Bot 3")
        self.bot4 = Bot("Bot 4")
    def deal_pockets(self):
        for i in range(2):
            new_card = self.deck.deal_card()
            new_card2 = self.deck.deal_card()
            new_card3 = self.deck.deal_card()
            new_card4 = self.deck.deal_card()
            self.bot1.hand.add_card(new_card)
            self.bot1.all_cards.append(new_card)
            self.bot2.hand.add_card(new_card2)
            self.bot2.all_cards.append(new_card2)
            self.bot3.hand.add_card(new_card3)
            self.bot3.all_cards.append(new_card3)
            self.bot4.hand.add_card(new_card4)
            self.bot4.all_cards.append(new_card4)
        self.bot1.eval_hand()
        self.bot2.eval_hand()
        self.bot3.eval_hand()
        self.bot4.eval_hand()
    def deal_flop(self):
        for i in range(3):
            new_card = self.deck.deal_card()
            self.middle.add_card(new_card)
            self.bot1.all_cards.append(new_card)
            self.bot2.all_cards.append(new_card)
            self.bot3.all_cards.append(new_card)
            self.bot4.all_cards.append(new_card)
        print(f"The flop is a {turn_to_str(self.middle.cards[0].val)} of {self.middle.cards[0].suit}, a {turn_to_str(self.middle.cards[1].val)} of {self.middle.cards[1].suit}, and a {turn_to_str(self.middle.cards[2].val)} of {self.middle.cards[2].suit}")
        self.bot1.calc_strength()
        self.bot2.calc_strength()
        self.bot3.calc_strength()
        self.bot4.calc_strength()
    def deal_turn(self):
        new_card = self.deck.deal_card()
        self.middle.add_card(new_card)
        self.bot1.all_cards.append(new_card)
        self.bot2.all_cards.append(new_card)
        self.bot3.all_cards.append(new_card)
        self.bot4.all_cards.append(new_card)
        print(f"The turn is a {turn_to_str(self.middle.cards[3].val)} of {self.middle.cards[3].suit}")
        self.bot1.calc_strength()
        self.bot2.calc_strength()
        self.bot3.calc_strength()
        self.bot4.calc_strength()
    def deal_river(self):
        new_card = self.deck.deal_card()
        self.middle.add_card(new_card)
        self.bot1.all_cards.append(new_card)
        self.bot2.all_cards.append(new_card)
        self.bot3.all_cards.append(new_card)
        self.bot4.all_cards.append(new_card)
        print(f"The river is a {turn_to_str(self.middle.cards[4].val)} of {self.middle.cards[4].suit}")
        self.bot1.calc_strength()
        self.bot2.calc_strength()
        self.bot3.calc_strength()
        self.bot4.calc_strength()
    def calc_final(self):
        self.final_hands = final_hands
        self.final_hands.sort(key=lambda bot: bot.final_num)
        print(f"The winner of this round is {final_hands[-1].name} with a {final_hands[-1].best}")




round = Round()
round.deal_pockets()
round.deal_flop()
round.deal_turn()
round.deal_river()
round.bot1.end_game()
round.bot2.end_game()
round.bot3.end_game()
round.bot4.end_game()
round.calc_final()
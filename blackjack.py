import random
import time
import sys
balance = 0
high_player_hands = []
low_player_hands = []
suits = ["spades", "clubs", "diamonds", "hearts"]
def split():
    """
    This function is called when the player has two cards with the same value,
    and they choose to split them. The player's hand is split into two
    separate hands, and they are given a new card for each hand.
    """
    global player_card1
    global player_card2
    global low_player_hand
    global bet_amount
    global balance

    # The player's balance is reduced by the amount of their bet
    balance = balance - int(bet_amount)

    if player_card1 == 1:
        # If the first card is an ace, the player is given a new card
        new_card = random.randrange(1, 14)
        new_suit = random.randrange(0, 4)
        print("You drew a", end="")
        if new_card == 11:
            print(" (J)ack", end=" ")
            new_card = 10
        elif new_card == 12:
            print(" (Q)ueen", end=" ")
            new_card = 10
        elif new_card == 13:
            print(" (K)ing", end=" ")
            new_card = 10
        elif new_card == 1:
            print("n (A)ce", end=" ")
        else:
            print(end=" ")
            print(new_card, end=" ")
        print(" of ", end="")
        print(suits[new_suit], end=" ")
        player_card1 = 11 + new_card
        print("for the first (A)ce. You now have ", end="")
        print(player_card1, end="")
        print(" for that one")
        # The player's hand is split into two separate hands
        high_player_hands.append(player_card1)
        time.sleep(1)
        # The player is given a new card for the second hand
        new_card2 = random.randrange(1, 14)
        new_suit2 = random.randrange(0, 4)
        print("You drew a", end="")
        if new_card2 == 11:
            print(" (J)ack", end=" ")
            new_card2 = 10
        elif new_card2 == 12:
            print(" (Q)ueen", end=" ")
            new_card2 = 10
        elif new_card2 == 13:
            print(" (K)ing", end=" ")
            new_card2 = 10
        elif new_card2 == 1:
            print("n (A)ce", end=" ")
        else:
            print(end=" ")
            print(new_card2, end=" ")
        print(" of ", end="")
        print(suits[new_suit2], end=" ")
        player_card2 = 11 + new_card2
        print("for the second (A)ce. You now have ", end="")
        print(player_card2, end="")
        print(" for that one")
        # The player's second hand is appended to the list of player hands
        high_player_hands.append(player_card2)
        # The dealer's hand is played
        computer_plays()
    else:
        # If the first card is not an ace, the player is given a new card
        new_suit = random.randrange(0, 4)
        new_card = random.randrange(1, 14)
        print("You drew a", end="")
        if new_card == 11:
            print(" (J)ack", end=" ")
            new_card = 10
        elif new_card == 12:
            print(" (Q)ueen", end=" ")
            new_card = 10
        elif new_card == 13:
            print(" (K)ing", end=" ")
            new_card = 10
        elif new_card == 1:
            print("n (A)ce", end=" ")
            new_card = 11
        else:
            print(end=" ")
            print(new_card, end=" ")
        print(" of ", end="")
        print(suits[new_suit], end=" ")
        player_hand1 = player_card1 + new_card
        print("for the first card. You now have ", end="")
        print(player_hand1, end="")
        print(" for that one")
        time.sleep(1)
        # The player is given a new card for the second hand
        new_card2 = random.randrange(1, 14)
        new_suit2 = random.randrange(0, 4)
        print("You drew a", end="")
        if new_card2 == 11:
            print(" (J)ack", end=" ")
            new_card2 = 10
        elif new_card2 == 12:
            print(" (Q)ueen", end=" ")
            new_card2 = 10
        elif new_card2 == 13:
            print(" (K)ing", end=" ")
            new_card2 = 10
        elif new_card2 == 1:
            print("n (A)ce", end=" ")
            new_card2 = 11
        else:
            print(end=" ")
            print(new_card2, end=" ")
        print(" of ", end="")
        print(suits[new_suit2], end=" ")
        player_hand2 = player_card2 + new_card2
        print("for the second card. You now have ", end="")
        print(player_hand2, end="")
        print(" for that one. Time to make your bets")
        print("For the first one: ")
        # The player is asked to make a bet for the first hand
        first_bet(player_card1, new_card, player_hand1, 0, 0)
        print("And for the second one: ")
        # The player is asked to make a bet for the second hand
        first_bet(player_card2, new_card2, player_hand2, 0, 1)
def end_game():
    """
    This function determines the winner of each hand and adds the 
    winnings to the player's balance. If the player's balance is zero, 
    the game ends.
    """
    global high_comp_hand
    global high_player_hands
    global low_comp_hand
    global low_player_hand
    global bet_amount
    global balance
    
    # For each hand that the player split
    for i in range(0, len(high_player_hands)):
        
        # If the player does not have an ace
        if low_player_hands[i] == 0 and low_comp_hand == 0:
            # If the dealer's hand is higher, the dealer wins
            if high_comp_hand > high_player_hands[i]:
                print("The dealer won with a ", end="")
                print(high_comp_hand, end="")
                print(" over your ", end="")
                print(high_player_hands[i])
            # If the dealer's hand is lower, the player wins
            elif high_comp_hand < high_player_hands[i]:
                print("You won with a ", end="")
                print(high_player_hands[i], end="")
                print(" over the dealer's ", end="")
                print(high_comp_hand)
                balance = balance + int(bet_amount) * 2
                print("Your balance is now ", end="")
                print(balance)
                
            # If the dealer and player have the same hand, it's a push
            else:
                print("You pushed with the dealer")
                balance = balance + int(bet_amount)
                print("Your balance is now ", end="")
                print(balance)
                
        # If the player has an ace and the dealer does not
        elif low_player_hands[i] > 0 and low_comp_hand == 0:
            # If the player's hand is higher, the player wins
            if high_player_hands[i] > 21:
                if high_comp_hand > low_player_hands[i]:
                    print("The dealer won with a ", end="")
                    print(high_comp_hand, end="")
                    print(" over your ", end="")
                    print(low_player_hands[i])
                elif high_comp_hand < low_player_hands[i]:
                    print("You won with a ", end="")
                    print(low_player_hands[i], end="")
                    print(" over the dealer's ", end="")
                    print(high_comp_hand)
                    balance = balance + int(bet_amount) * 2
                    print("Your balance is now ", end="")
                    print(balance)
                elif high_comp_hand > 21:
                    print("The dealer busted")
                    balance = balance + int(bet_amount) * 2
                    print("Your balance is now ", end="")
                    print(balance)
                else:
                    print("You pushed with the dealer")
                    balance = balance + int(bet_amount)
                    print("Your balance is now ", end="")
                    print(balance)
            else:
                if high_comp_hand > high_player_hands[i]:
                    print("The dealer won with a ", end="")
                    print(high_comp_hand, end="")
                    print(" over your ", end="")
                    print(high_player_hands[i])
                elif high_comp_hand < high_player_hands[i]:
                    print("You won with a ", end="")
                    print(high_player_hands[i], end="")
                    print(" over the dealer's ", end="")
                    print(high_comp_hand)
                    balance = balance + int(bet_amount) * 2
                    print("Your balance is now ", end="")
                    print(balance)
                else:
                    print("You pushed with the dealer")
                    balance = balance + int(bet_amount)
                    print("Your balance is now ", end="")
                    print(balance)
        # If the player does not have an ace and the dealer does
        elif low_player_hands[i] == 0 and low_comp_hand > 0:
            
            if high_comp_hand > 21:
                if low_comp_hand > high_player_hands[i]:
                    print("The dealer won with a ", end="")
                    print(low_comp_hand, end="")
                    print(" over your ", end="")
                    print(high_player_hands[i])
                elif low_comp_hand < high_player_hands[i]:
                    print("You won with a ", end="")
                    print(high_player_hands[i], end="")
                    print(" over the dealer's ", end="")
                    print(low_comp_hand)
                    balance = balance + int(bet_amount) * 2
                    print("Your balance is now ", end="")
                    print(balance)
                    
                else:
                    print("You pushed with the dealer")
                    balance = balance + int(bet_amount)
                    print("Your balance is now ", end="")
                    print(balance)
                    
            else:
                if high_comp_hand > high_player_hands[i]:
                    print("The dealer won with a ", end="")
                    print(high_comp_hand, end="")
                    print(" over your ", end="")
                    print(high_player_hands[i])
                elif high_comp_hand < high_player_hands[i]:
                    print("You won with a ", end="")
                    print(high_player_hands[i], end="")
                    print(" over the dealer's ", end="")
                    print(high_comp_hand)
                    balance = balance + int(bet_amount) * 2
                    print("Your balance is now ", end="")
                    print(balance)
                    
                else:
                    print("You pushed with the dealer")
                    balance = balance + int(bet_amount)
                    print("Your balance is now ", end="")
                    print(balance)
                    
        else:
            if high_comp_hand > 21 and high_player_hands[i] <= 21:
                if low_comp_hand > high_player_hands[i]:
                    print("The dealer won with a ", end="")
                    print(low_comp_hand, end="")
                    print(" over your ", end="")
                    print(high_player_hands[i])
                elif low_comp_hand < high_player_hands[i]:
                    print("You won with a ", end="")
                    print(high_player_hands[i], end="")
                    print(" over the dealer's ", end="")
                    print(low_comp_hand)
                    balance = balance + int(bet_amount) * 2
                    print("Your balance is now ", end="")
                    print(balance)
                else:
                    print("You pushed with the dealer")
                    balance = balance + int(bet_amount)
            elif high_player_hands[i] <= 21 and high_comp_hand <= 21:
                if high_comp_hand > high_player_hands[i]:
                    print("The dealer won with a ", end="")
                    print(high_comp_hand, end="")
                    print(" over your ", end="")
                    print(high_player_hands[i])
                elif high_comp_hand < high_player_hands[i]:
                    print("You won with a ", end="")
                    print(high_player_hands[i], end="")
                    print(" over the dealer's ", end="")
                    print(high_comp_hand)
                    balance = balance + int(bet_amount) * 2
                    print("Your balance is now ", end="")
                    print(balance)
                else:
                    print("You pushed with the dealer")
                    balance = balance + int(bet_amount)
                    print("Your balance is now ", end="")
                    print(balance)
            elif high_comp_hand <= 21 and high_player_hands[i] > 21:
                if high_comp_hand > low_player_hands[i]:
                    print("The dealer won with a ", end="")
                    print(high_comp_hand, end="")
                    print(" over your ", end="")
                    print(low_player_hands[i])
                elif high_comp_hand < low_player_hands[i]:
                    print("You won with a ", end="")
                    print(low_player_hands[i], end="")
                    print(" over the dealer's ", end="")
                    print(high_comp_hand)
                    balance = balance + int(bet_amount) * 2
                    print("Your balance is now ", end="")
                    print(balance)
                else:
                    print("You pushed with the dealer")
                    balance = balance + int(bet_amount)
                    print("Your balance is now ", end="")
                    print(balance)
            else:
                if low_comp_hand > low_player_hands[i]:
                    print("The dealer won with a ", end="")
                    print(low_comp_hand, end="")
                    print(" over your ", end="")
                    print(low_player_hands[i])
                elif low_comp_hand < low_player_hands[i]:
                    print("You won with a ", end="")
                    print(low_player_hands[i], end="")
                    print(" over the dealer's ", end="")
                    print(low_comp_hand)
                    balance = balance + int(bet_amount) * 2
                    print("Your balance is now ", end="")
                    print(balance)
                else:
                    print("You pushed with the dealer")
                    balance = balance + int(bet_amount)
                    print("Your balance is now ", end="")
                    print(balance)
    
    print("Your balance is now ", end="")
    print(balance, end=". ")
    play_again = input("Would you like to play another hand? Y/N")
    if play_again.lower() == "y":
        play()
    else:
        print("Okay, see you later!")
        sys.exit()
def first_bet(card1, card2, high_hand, low_hand, splitted):
    """
    This function is the first part of the player's turn. It asks the player
    if they want to hit, double down, stand, or split if their cards have the
    same value.
    """
    global balance
    global bet_amount
    print("Would you like to ")
    print("[1] Hit")
    print("[2] Double Down")
    print("[3] Stand")
    if card2 == card1:
        print("[4] Split")
    decision = input("")
    if int(decision) == 1:
        """
        If the player chooses to hit, a new card is drawn and added to their
        hand total. If the player has an ace in their hand, the ace is
        counted as 11 unless the total is already over 21, in which case it
        is counted as 1.
        """
        new_card = random.randrange(1, 14)
        new_suit = random.randrange(0, 4)
        print("You got a ", end="")
        if new_card == 11:
            print("(J)ack", end="")
            new_card = 10
        elif new_card == 12:
            print("(Q)ueen", end="")
            new_card = 10
        elif new_card == 13:
            print("(Q)ueen", end="")
            new_card = 10
        elif new_card == 1:
            print("(A)ce", end="")
            if high_hand > 10:
                new_card = 1
            else:
                new_card = 11
                low_hand = high_hand + 1
        else:
            print(new_card, end="")
        print(" of ", end="")
        print(suits[new_suit], end="")
        high_hand = high_hand + new_card
        print(" for a ", end="")
        if low_hand > 0:
            low_hand = low_hand + new_card
            print(low_hand, end="")
            print("/", end="")
        print(high_hand)
        if high_hand > 21:
            """
            If the player busts, they lose the hand. If the player has an ace
            in their hand, the ace is counted as 1 and the player is given
            another chance to hit.
            """
            if low_hand > 0:
                other_bets(high_hand, low_hand, splitted)
            else:
                if splitted == 1:
                    print("You busted. Better luck next time!")
                    print("Your balance is now ", end="")
                    print(balance, end=". ")
                    play_again = input("Would you like to play another hand? Y/N")
                    if play_again.lower() == "y":
                        play()
                    else:
                        print("Okay, see you later!")
                        sys.exit()
        else:
            """
            If the player does not bust, they are given another chance to hit.
            """
            other_bets(high_hand, low_hand, splitted)
    elif int(decision) == 2:
        """
        If the player chooses to double down, their bet is doubled and they
        are given one more card. The player's turn is then over.
        """
        balance = balance - int(bet_amount)
        bet_amount = int(bet_amount) * 2
        new_card = random.randrange(1, 14)
        new_suit = random.randrange(0, 4)
        print("You got a ", end="")
        if new_card == 11:
            print("(J)ack", end="")
            new_card = 10
        elif new_card == 12:
            print("(Q)ueen", end="")
            new_card = 10
        elif new_card == 13:
            print("(K)ing", end="")
            new_card = 10
        elif new_card == 1:
            if high_hand + new_card > 21:
                new_card = 1
            else:
                new_card = 11
        else:
            print(new_card, end="")
        print(" of ", end="")
        print(suits[new_suit], end="")
        high_hand = high_hand + new_card
        print(" for a ", end="")
        if low_hand > 0:
            low_hand = low_hand + new_card
            print(low_hand, end="")
            print("/", end="")
        print(high_hand)
        if high_hand > 21 and splitted == 1:
            print("You busted. Better luck next time!")
            print("Your balance is now ", end="")
            print(balance, end=". ")
            play_again = input("Would you like to play another hand? Y/N")
            if play_again.lower() == "y":
                play()
            else:
                print("Okay, see you later!")
                sys.exit()
        else:
            if splitted == 1:
                computer_plays()
            high_player_hands.append(high_hand)
            low_player_hands.append(low_hand)
    elif int(decision) == 3:
        """
        If the player chooses to stand, their turn is over and the dealer's
        turn begins.
        """
        high_player_hands.append(high_hand)
        low_player_hands.append(low_hand)
        if splitted == 1:
            computer_plays()
    else:
        """
        If the player chooses to split, their hand is split into two separate
        hands and each hand is given a new card. The player's turn is then over.
        """
        split()
def other_bets(high_hand, low_hand, splitted):
    """
    This function is called by the main play() function after the player's
    first bet. It asks the player what they want to do with their hand.
    """
    global balance
    global bet_amount

    # Ask the player if they want to hit or stand
    print("Would you like to ")
    print("[1] Hit")
    print("[2] Stand")
    decision = input("")

    # If the player wants to hit
    if int(decision) == 1:
        # Get a new card
        new_card = random.randrange(1, 14)
        new_suit = random.randrange(0, 4)
        print("You got a ", end="")

        # If the card is a jack, queen, king, or ace
        if new_card == 11:
            print("(J)ack", end="")
            new_card = 10
        elif new_card == 12:
            print("(Q)ueen", end="")
            new_card = 10
        elif new_card == 13:
            print("(K)ing", end="")
            new_card = 10
        elif new_card == 1:
            print("(A)ce", end="")
            # If the player does not have an ace in their hand
            if low_hand == 0:
                # Give the player an ace in the low hand
                low_hand = high_hand + 1
                # Add 11 to the high hand
                high_hand = high_hand + 11
            # If the player's low hand is less than 21 and the player has an
            # ace in their hand
            if (low_hand + 11) < 21 and low_hand > 0:
                # Add 11 to the low hand
                low_hand = low_hand + 11
        else:
            print(new_card, end="")
        print(" of ", end="")
        print(suits[new_suit], end="")
        # Add the new card to the player's high hand
        high_hand = high_hand + new_card

        # If the player has an ace in their low hand
        if low_hand > 0 and new_card > 1:
            # Add the new card to the player's low hand
            low_hand = low_hand + new_card
        # Print the player's hand
        print(" for a ", end="")
        if low_hand > 0:
            print(low_hand, end="")
            print("/", end="")
        print(high_hand)

        # If the player has busted
        if high_hand > 21:
            # If the player has an ace in their low hand
            if low_hand == 0 or low_hand > 21 and splitted == 1:
                # Tell the player they busted
                print("You busted. Better luck next time!")
                print("Your balance is now ", end="")
                print(balance, end=". ")
                play_again = input("Would you like to play another hand? Y/N")
                if play_again.lower() == "y":
                    play()
                else:
                    print("Okay, see you later!")
                    sys.exit()
            else:
                # Otherwise, call this function again to let the player
                # continue their turn
                other_bets(high_hand, low_hand, splitted)
        else:
            # Call this function again to let the player continue their turn
            other_bets(high_hand, low_hand, splitted)
    else:
        # Add the player's hand to the list of player hands
        high_player_hands.append(high_hand)
        low_player_hands.append(low_hand)

        # If the player split their hand
        if splitted == 1:
            # Call the computer_plays() function
            computer_plays()  
def computer_plays():
    """
    This function is called after the player has finished their turn. It
    determines the dealer's hand and compares it to the player's hand to
    determine who wins.
    """
    global low_comp_hand
    global high_comp_hand
    global comp_card2
    global comp_suit2
    global comp_card1
    global comp_suit1
    global balance
    global bet_amount
    comp_suit2 = random.randrange(0, 4)


    # Print out the dealer's up card
    print("The delear has a ", end="")
    if comp_card2 == 11:
        print("(J)ack", end="")
        comp_card2 = 10
    elif comp_card2 == 12:
        print("(Q)ueen", end="")
        comp_card2 = 10
    elif comp_card2 == 13:
        print("(K)ing", end="")
        comp_card2 = 10
    elif comp_card2 == 1:
        print("(A)ce", end="")
        low_comp_hand = comp_card1 + 1
        high_comp_hand = comp_card1 + 11
    else:
        print(comp_card2, end="")
    print(" of ", end="")
    print(suits[comp_suit2], end="")
    print(" for a ", end="")
    if low_comp_hand > 0:
        print(low_comp_hand, end="/")
    print(high_comp_hand)

    # While the dealer's hand is less than 17, deal them a card
    while high_comp_hand < 17:
        time.sleep(1.5)
        new_card = random.randrange(1, 14)
        new_suit = random.randrange(0, 4)
        print("The dealer got a", end="")
        if new_card == 11:
            print(" (J)ack", end="")
            new_card = 10
        elif new_card == 12:
            print(" (Q)ueen", end="")
            new_card = 10
        elif new_card == 13:
            print(" (Q)ueen", end="")
            new_card = 10
        elif new_card == 1:
            print("n (A)ce", end="")
            high_comp_hand = high_comp_hand + 11
            low_comp_hand = low_comp_hand + 1
        else:
            print(" ", end="")
            print(new_card, end="")
        print(" of ")
        print(suits[new_suit], end="")
        high_comp_hand = high_comp_hand + new_card
        print(" for a ", end="")
        if low_comp_hand > 0:
            low_comp_hand = low_comp_hand + new_card
            print(low_comp_hand, end="")
            print("/", end="")
        print(high_comp_hand)

    # If the dealer's hand is exactly 17 and they have an ace, deal them
    # another card
    if high_comp_hand == 17 and low_comp_hand > 0:
        new_card = random.randrange(1, 14)
        new_suit = random.randrange(0, 4)
        print("The dealer got a ", end="")
        if new_card == 11:
            print("(J)ack", end="")
            new_card = 10
        elif new_card == 12:
            print("(Q)ueen", end="")
            new_card = 10
        elif new_card == 13:
            print("(Q)ueen", end="")
            new_card = 10
        else:
            print(new_card, end="")
        low_comp_hand = low_comp_hand + new_card
        print(" of ", end="")
        print(suits[new_suit], end="")
        print(" for a ", end="")
        print(low_comp_hand)

    # If the dealer busts, the player wins
    if high_comp_hand > 21:
        if low_comp_hand == 0:
            print("The dealer busted. You Win!")
            balance = balance + int(bet_amount) * 2
            
            print("Your balance is now ", end="")
            print(balance, end=". ")
            play_again = input("Would you like to play another hand? Y/N")
            if play_again.lower() == "y":
                play()
            else:
                print("Okay, see you later!")
                sys.exit()
        else:
            while low_comp_hand < 17:
                new_card = random.randrange(1, 14)
                print("The dealer got a ", end="")
                if new_card == 11:
                    print("(J)ack", end="")
                    new_card = 10
                elif new_card == 12:
                    print("(Q)ueen", end="")
                    new_card = 10
                elif new_card == 13:
                    print("(Q)ueen", end="")
                    new_card = 10
                else:
                    print(new_card, end="")
                low_comp_hand = low_comp_hand + new_card
                print(" for a ", end="")
                print(low_comp_hand)
            if low_comp_hand > 21:
                print("the dealer busted. You win!")
                balance = balance + int(bet_amount) * 2
                print("Your balance is now ", end="")
                print(balance, end=". ")
                play_again = input("Would you like to play another hand? Y/N")
                if play_again.lower() == "y":
                    play()
                else:
                    print("Okay, see you later!")
                    sys.exit()
            else:
                end_game()
    else:
        end_game()
    end_game()
def bet():
    global bet_amount
    global balance
    bet_amount = 0
    bet_amount = input("How much would you like to bet on this hand: ")
    if int(bet_amount) > balance:
        print("Your balance is not great enough for that bet. Please adjust your bet to continue")
        update_balance()
    else:
        balance = balance - int(bet_amount)
def update_balance():
    global bet_amount
    global balance
    print("Your balance is currently ", end="")
    print(balance, end="")
    prelim = input(". Would you like to update your balance? Y/N")
    if prelim.lower() == "y":
        added_money = input("How much would you like to add to you balance: ")
        balance = balance + int(added_money)
        play()
    else:
        if balance == 0:
            print("Ok, see you later!")
        else:
            bet()
def play():
    #clear the data for hands
    high_player_hands.clear()
    low_player_hands.clear()
    """
    This is the main function of the blackjack game. It determines the initial
    hands of the player and dealer, and then asks the player what they want to
    do with their hand.
    """
    global balance
    if balance == 0:
        update_balance()
    bet()
    print("Shuffling...")
    time.sleep(3)
    print("Dealing...")
    time.sleep(2)
    global high_comp_hand
    global low_comp_hand
    global high_player_hand
    global low_player_hand
    global comp_card1
    global comp_card2
    global player_card1
    global player_card2
    """
    Determine the dealer's hand
    """
    comp_card1 = random.randrange(1, 14)
    comp_suit1 = random.randrange(0, 4)
    comp_card2 = random.randrange(1, 14)
    """
    Determine the player's hand
    """
    player_card1 = random.randrange(1, 14)
    player_suit1 = random.randrange(0, 4)
    player_card2 = random.randrange(1, 14)
    player_suit2 = random.randrange(0, 4) 
    high_comp_hand = 0
    low_comp_hand = 0
    high_player_hand = 0
    low_player_hand = 0
    print("The dealer has a ", end="")
    if comp_card1 == 11:
        print("(J)ack", end="")
        comp_card1 = 10
        if comp_card2 == 1:
            print("The dealer has blackjack")
            high_comp_hand = 50
    elif comp_card1 == 12:
        print("(Q)ueen", end="")
        comp_card1 = 10
        if comp_card2 == 1:
            print("The dealer has blackjack")
            high_comp_hand = 50
    elif comp_card1 == 13:
        print("(K)ing, end=")
        comp_card1 = 10
        if comp_card2 == 1:
            print("The dealer has blackjack")
            high_comp_hand = 50
    elif comp_card1 == 1:
        print("(A)ce", end="")
        low_comp_hand = comp_card2 + 1
        high_comp_hand = comp_card2 + 11
        time.sleep(1)
        if comp_card2 == 10 or comp_card2 == 11 or comp_card2 == 12 or comp_card2 == 13:
            print("The dealer has blackjack")
            high_comp_hand = 50
    else:
        print(comp_card1, end="")
    print(" of ", end="")
    print(suits[comp_suit1])
    if high_comp_hand < 50:
        high_comp_hand = comp_card2 + comp_card1
    print("You have a ", end="")
    if player_card1 == 11:
        print("(J)ack", end="")
        player_card1 = 10
    elif player_card1 == 12:
        print("(Q)ueen", end="")
        player_card1 = 10
    elif player_card1 == 13:
        print("(K)ing", end="")
        player_card1 = 10
    elif player_card1 == 1:
        print("(A)ce", end="")
        low_player_hand = player_card2 + 1
        player_card1 = 11
    else:
        print(player_card1, end="")
    print(" of ", end="")
    print(suits[player_suit1], end="")
    print(" and a ", end="")
    if player_card2 == 11:
        print("(J)ack", end="")
        player_card2 = 10
        high_player_hand = player_card1 + player_card2
    elif player_card2 == 12:
        print("(Q)ueen", end="")
        player_card2 = 10
        high_player_hand = player_card1 + player_card2
    elif player_card2 == 13:
        print("(K)ing", end="")
        player_card2 = 10
        high_player_hand = player_card1 + player_card2
    elif player_card2 == 1:
        print("(A)ce", end="")
        time.sleep(1)
        if player_card1 == 11:
            player_card1 = 1
        low_player_hand = player_card1 + 1
        high_player_hand = player_card1 + 11
    else:
        print(player_card2, end="")
        high_player_hand = player_card1 + player_card2
    print(" of ", end="")
    print(suits[player_suit2], end="")
    print(" for a ", end="")
    if low_player_hand == 0:
        if high_comp_hand < 50:
            print(high_player_hand)
            first_bet(player_card1, player_card2, high_player_hand, low_player_hand, 1)
        else:
            print("not blackjack. You lost. Better luck next time!")
            print("Your balance is now ", end="")
            print(balance, end=". ")
            play_again = input("Would you like to play another hand? Y/N")
            if play_again.lower() == "y":
                play()
            else:
                print("Okay, see you later!")
                sys.exit()
    elif high_player_hand == 21:
        print("blackjack!")
        high_player_hand = 50
    else:
        if high_comp_hand < 50:
            print(low_player_hand, end="")
            print("/", end="")
            print(high_player_hand)
            first_bet(player_card1, player_card2, high_player_hand, low_player_hand, 1)
        else:
            print("You lost. Better luck next time!")
            print("Your balance is now ", end="")
            print(balance, end=". ")
            play_again = input("Would you like to play another hand? Y/N")
            if play_again.lower() == "y":
                play()
            else:
                print("Okay, see you later!")
                sys.exit()
play()

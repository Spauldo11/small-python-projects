import random
def play():
    comp = random.randrange(0,3)
    selection = input("Rock, Paper, or Scissors")
    if selection.lower() == "rock":
        win = "scissors"
        tie = "rock"
        loss = "paper"
    elif selection.lower() == "paper":
        win = "rock"
        tie = "paper"
        loss = "scissors"
    elif selection.lower() == "scissors":
        win = "paper"
        tie = "scissors"
        loss = "rock"
    else:
        print("You inputted your choice wrong. Please try again")
    if comp == 0:
        print("You won! Your opponent chose ", end="")
        print(win)
    elif comp == 1:
        print("You tied! Your opponent chose ", end="")
        print(tie)
    else:
        print("You lost! Your opponent chose ", end="")
        print(loss)
    play_again = input("Would you like to play again? Y/N")
    if play_again.lower() == "y":
        play()
    else:
        print("Okay, come back and play again soon!")
play()
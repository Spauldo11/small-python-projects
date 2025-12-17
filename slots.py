import random
import time
import pygame
# using an array like this, you can ensure which number outcomes are most and least common
options = ['A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'C', 'C', 'C', 'D', 'D', '7']
balance = 1000
bet_amount = 10
running = True

def display():
    screen.fill(white)
    # renders rectangles to form the grid
    pygame.draw.rect(screen, "black", (0, screen.get_height()/4, 11000, 50))
    pygame.draw.rect(screen, "black", (0, (screen.get_height()/3)*2, 11000, 50))
    pygame.draw.rect(screen, "black", ((screen.get_width()/3)*2+25, 0, 50, 9000))
    pygame.draw.rect(screen, "black", (screen.get_width()/3-45, 0, 50, 9000))
    # displays your current balance
    balance_text = mini_font.render("Balance: ", True, (0, 0, 0))
    money = mini_font.render(str(balance), True, (0, 0, 0))
    # all of the numbers on the grid displayed with their respective color
    num_one = font.render(num1, True, num1_color)
    num_two = font.render(num2, True, num2_color)
    num_three = font.render(num3, True, num3_color)
    num_four = font.render(num4, True, num4_color)
    num_five = font.render(num5, True, num5_color)
    num_six = font.render(num6, True, num6_color)
    num_seven = font.render(num7, True, num7_color)
    num_eight = font.render(num8, True, num8_color)
    num_nine = font.render(num9, True, num9_color)
    # render everything on screen
    screen.blit(balance_text, (10, 10))
    screen.blit(money, (140, 10))
    screen.blit(num_one, (90, 55))
    screen.blit(num_two, (510, 55))
    screen.blit(num_three, (900, 55))
    screen.blit(num_four, (90, 400))
    screen.blit(num_five, (510, 400))
    screen.blit(num_six, (900, 400))
    screen.blit(num_seven, (90, 750))
    screen.blit(num_eight, (510, 750))
    screen.blit(num_nine, (900, 750))
    pygame.display.flip()


def change_nums():
    num1 = options[random.randint(0, 14)]
    num2 = options[random.randint(0, 14)]
    num3 = options[random.randint(0, 14)]
    num4 = options[random.randint(0, 14)]
    num5 = options[random.randint(0, 14)]
    num6 = options[random.randint(0, 14)]
    num7 = options[random.randint(0, 14)]
    num8 = options[random.randint(0, 14)]
    num9 = options[random.randint(0, 14)]
    nums = [[num1, num2, num3], [num4, num5, num6], [num7, num8, num9]]
    return nums


# Generate new grid
def spin(bet_amount):
    global balance
    global num1, num2, num3, num4, num5, num6, num7, num8, num9
    global nums
    num1 = options[random.randint(0, 14)]
    num2 = options[random.randint(0, 14)]
    num3 = options[random.randint(0, 14)]
    num4 = options[random.randint(0, 14)]
    num5 = options[random.randint(0, 14)]
    num6 = options[random.randint(0, 14)]
    num7 = options[random.randint(0, 14)]
    num8 = options[random.randint(0, 14)]
    num9 = options[random.randint(0, 14)]
    nums = [[num1, num2, num3], [num4, num5, num6], [num7, num8, num9]]
    winnings = 0
    balance = int(balance) - int(bet_amount)
    # check if there are three matching in a row
    if num1 == num2 and num2 == num3:
        match num1:
            # depending on what letter it is, your bet is multiplied by more
            case 'A':
                factor = 1.2
            case 'B':
                factor = 1.5
            case 'C':
                factor = 2.5
            case 'D':
                factor = 6.5
            case _:
                factor = 10
        # add to the total winnings of that spin
        winnings = winnings + (int(bet_amount) * factor)
    # the previous comments apply for all the code until line 184
    if num1 == num4 and num4 == num7:
        match num1:
            case 'A':
                factor = 1.2
            case 'B':
                factor = 1.5
            case 'C':
                factor = 2.5
            case 'D':
                factor = 6.5
            case _:
                factor = 10
        winnings = winnings + (int(bet_amount) * factor)
    if num4 == num5 and num5 == num6:
        match num4:
            case 'A':
                factor = 1.2
            case 'B':
                factor = 1.5
            case 'C':
                factor = 2.5
            case 'D':
                factor = 6.5
            case _:
                factor = 10
        winnings = winnings + (int(bet_amount) * factor)
    if num2 == num5 and num5 == num8:
        match num2:
            case 'A':
                factor = 1.2
            case 'B':
                factor = 1.5
            case 'C':
                factor = 2.5
            case 'D':
                factor = 6.5
            case _:
                factor = 10
        winnings = winnings + (int(bet_amount) * factor)
    if num7 == num8 and num8 == num9:
        match num7:
            case 'A':
                factor = 1.2
            case 'B':
                factor = 1.5
            case 'C':
                factor = 2.5
            case 'D':
                factor = 6.5
            case _:
                factor = 10
        winnings = winnings + (int(bet_amount) * factor)
    if num3 == num6 and num6 == num9:
        match num6:
            case 'A':
                factor = 1.2
            case 'B':
                factor = 1.5
            case 'C':
                factor = 2.5
            case 'D':
                factor = 6.5
            case _:
                factor = 10
        winnings = winnings + (int(bet_amount) * factor)
    if num1 == num5 and num5 == num9:
        match num5:
            case 'A':
                factor = 1.2
            case 'B':
                factor = 1.5
            case 'C':
                factor = 2.5
            case 'D':
                factor = 6.5
            case _:
                factor = 10
        winnings = winnings + (int(bet_amount) * factor)
    if num3 == num5 and num5 == num7:
        match num5:
            case 'A':
                factor = 1.2
            case 'B':
                factor = 1.5
            case 'C':
                factor = 2.5
            case 'D':
                factor = 6.5
            case _:
                factor = 10
        winnings = winnings + (int(bet_amount) * factor)
    balance = balance + winnings
pygame.init()
pygame.mixer.init()
ding = pygame.mixer.Sound("short_bing.wav")
end_sound = pygame.mixer.Sound("long_finish_bells.wav")
screen = pygame.display.set_mode((1100, 1000))
clock = pygame.time.Clock()
white = 255, 255, 255
font = pygame.font.SysFont("Arial", 180)
mini_font = pygame.font.SysFont("Arial", 32)
spin(0)
num1_color = (0, 0, 0)
num2_color = (0, 0, 0)
num3_color = (0, 0, 0)
num4_color = (0, 0, 0)
num5_color = (0, 0, 0)
num6_color = (0, 0, 0)
num7_color = (0, 0, 0)
num8_color = (0, 0, 0)
num9_color = (0, 0, 0)

while running:
    # change color of matching numbers if there are any at the start
    if num1 == num2 and num2 == num3:
        num1_color = (242, 219, 13)
        num2_color = (242, 219, 13)
        num3_color = (242, 219, 13)
    if num1 == num4 and num4 == num7:
        num1_color = (242, 219, 13)
        num4_color = (242, 219, 13)
        num7_color = (242, 219, 13)
    if num4 == num5 and num5 == num6:
        num4_color = (242, 219, 13)
        num5_color = (242, 219, 13)
        num6_color = (242, 219, 13)
    if num2 == num5 and num5 == num8:
        num2_color = (242, 219, 13)
        num5_color = (242, 219, 13)
        num8_color = (242, 219, 13)
    if num7 == num8 and num8 == num9:
        num7_color = (242, 219, 13)
        num8_color = (242, 219, 13)
        num9_color = (242, 219, 13)
    if num3 == num6 and num6 == num9:
        num3_color = (242, 219, 13)
        num6_color = (242, 219, 13)
        num9_color = (242, 219, 13)
    if num1 == num5 and num5 == num9:
        num1_color = (242, 219, 13)
        num5_color = (242, 219, 13)
        num9_color = (242, 219, 13)
    if num3 == num5 and num5 == num7:
        num3_color = (242, 219, 13)
        num5_color = (242, 219, 13)
        num7_color = (242, 219, 13)
    # when enter is pressed, there is a new spin and all numbers turn to black
    if pygame.key.get_pressed()[pygame.K_RETURN]:
        num1_color = (0, 0, 0)
        num2_color = (0, 0, 0)
        num3_color = (0, 0, 0)
        num4_color = (0, 0, 0)
        num5_color = (0, 0, 0)
        num6_color = (0, 0, 0)
        num7_color = (0, 0, 0)
        num8_color = (0, 0, 0)
        num9_color = (0, 0, 0)
        for i in range(12):
            time.sleep(0.05*(i+1))
            ding.play()
            spin(0)
            display()
        end_sound.play()
        spin(10)
        # change color of matching numbers if there are any after each new spin
        if num1 == num2 and num2 == num3:
            num1_color = (242, 219, 13)
            num2_color = (242, 219, 13)
            num3_color = (242, 219, 13)
        if num1 == num4 and num4 == num7:
            num1_color = (242, 219, 13)
            num4_color = (242, 219, 13)
            num7_color = (242, 219, 13)
        if num4 == num5 and num5 == num6:
            num4_color = (242, 219, 13)
            num5_color = (242, 219, 13)
            num6_color = (242, 219, 13)
        if num2 == num5 and num5 == num8:
            num2_color = (242, 219, 13)
            num5_color = (242, 219, 13)
            num8_color = (242, 219, 13)
        if num7 == num8 and num8 == num9:
            num7_color = (242, 219, 13)
            num8_color = (242, 219, 13)
            num9_color = (242, 219, 13)
        if num3 == num6 and num6 == num9:
            num3_color = (242, 219, 13)
            num6_color = (242, 219, 13)
            num9_color = (242, 219, 13)
        if num1 == num5 and num5 == num9:
            num1_color = (242, 219, 13)
            num5_color = (242, 219, 13)
            num9_color = (242, 219, 13)
        if num3 == num5 and num5 == num7:
            num3_color = (242, 219, 13)
            num5_color = (242, 219, 13)
            num7_color = (242, 219, 13)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    display()
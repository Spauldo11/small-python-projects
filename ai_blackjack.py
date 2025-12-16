# THIS WAS CODED BY GOOGLE GEMINI
# After Gemini coded the majority of the project, I tweaked the UI and debugged it.
import pygame
import random
import sys

# --- Pygame Setup ---
pygame.init()

# Game Constants
SCREEN_WIDTH = 1700
SCREEN_HEIGHT = 800
CAPTION = "Blackjack (H17 Rule)"
FONT_NAME = "arial"

# Colors
GREEN = (39, 119, 68)  # Table Green
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)

# Card dimensions
CARD_WIDTH = 80
CARD_HEIGHT = 120
CARD_BORDER_RADIUS = 10

# Initialize screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(CAPTION)
clock = pygame.time.Clock()

# Fonts
font_large = pygame.font.SysFont(FONT_NAME, 36)
font_medium = pygame.font.SysFont(FONT_NAME, 24)
font_small = pygame.font.SysFont(FONT_NAME, 18)


# --- Game Logic Classes ---

class Card:
    """Represents a playing card."""
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        # Calculate value for non-Aces (10 for J, Q, K)
        if rank in ('J', 'Q', 'K'):
            self.value = 10
        elif rank == 'A':
            self.value = 11  # Ace starts as 11
        else:
            self.value = int(rank)

    def __str__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    """Represents a deck of 52 cards."""
    def __init__(self):
        self.suits = ('H', 'D', 'C', 'S')  # Hearts, Diamonds, Clubs, Spades
        self.ranks = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
        self.shuffle()

    def shuffle(self):
        """Shuffles the deck."""
        random.shuffle(self.cards)

    def deal_card(self):
        """Deals one card from the deck."""
        if not self.cards:
            self.__init__() # Reshuffle if deck is empty
        return self.cards.pop()

class Hand:
    """Represents a hand of cards (player or dealer)."""
    def __init__(self, is_dealer=False):
        self.cards = []
        self.is_dealer = is_dealer

    def add_card(self, card):
        """Adds a card to the hand."""
        self.cards.append(card)

    def calculate_value(self):
        """Calculates the best possible value of the hand, handling Aces (1 or 11)."""
        value = sum(card.value for card in self.cards)
        num_aces = sum(1 for card in self.cards if card.rank == 'A')

        # Adjust Ace values if total exceeds 21
        while value > 21 and num_aces > 0:
            value -= 10  # Change an Ace from 11 to 1
            num_aces -= 1
        
        return value

    def is_soft_17(self):
        """Checks if the hand is a 'soft 17' (17 with an Ace counted as 11)."""
        value = sum(card.value for card in self.cards)
        num_aces = sum(1 for card in self.cards if card.rank == 'A')

        # A hand is a soft 17 if:
        # 1. Its current value (with an Ace counted as 11) is 17
        # 2. It contains at least one Ace
        # 3. If the Ace were counted as 1, the total would be 7 (i.e., (17 - 11) + 1 = 7)
        
        if self.calculate_value() == 17 and num_aces > 0:
            # Check if 17 is reached because one Ace is 11 and others are 1s (if any)
            # The sum of non-Ace cards must be 6 for a Soft 17 (11 + 6 = 17)
            non_ace_sum = sum(card.value for card in self.cards if card.rank != 'A')
            if non_ace_sum == 6:
                 # Check if the calculated value is 17 before Ace reduction
                 # If value > 21 after initial sum, it's already reduced and can't be soft 17
                 initial_value = sum(card.value for card in self.cards)
                 return initial_value == 17

        return False

# --- Game Class (State Management) ---

class BlackjackGame:
    def __init__(self):
        self.player_balance = 1000
        self.current_bet = 0
        self.deck = Deck()
        self.dealer_hand = Hand(is_dealer=True)
        self.player_hands = []  # List of Hand objects, initially one
        self.current_hand_index = 0
        self.message = "Place your bet to start the hand."
        
        # Game States: BETTING, PLAYER_TURN, DEALER_TURN, RESULTS
        self.state = 'BETTING'
        self.bet_input = "0"
        self.bet_amount = 50 # Default bet for quick testing
        self.is_split_possible = False

    def reset_hand(self):
        """Resets hands, deck, and state for a new hand."""
        self.deck = Deck()
        self.dealer_hand = Hand(is_dealer=True)
        self.player_hands = []
        self.current_hand_index = 0
        self.message = "Place your bet to start the hand."
        self.state = 'BETTING'
        self.is_split_possible = False
        self.bet_input = str(self.bet_amount)

    def deal(self):
        """Deals the initial four cards."""
        self.player_hands.append(Hand())
        player_hand = self.player_hands[0]
        
        # Initial deal: P, D, P, D
        player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
        player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
        
        self.current_bet = self.bet_amount
        self.player_balance -= self.current_bet

        self.check_initial_blackjack()

    def check_initial_blackjack(self):
        """Checks for immediate Blackjack after the deal."""
        player_value = self.player_hands[0].calculate_value()
        dealer_value = self.dealer_hand.calculate_value()

        if player_value == 21 and dealer_value == 21:
            self.message = "Push! Both have Blackjack."
            self.player_balance += self.current_bet
            self.state = 'RESULTS'
        elif player_value == 21:
            # Player Blackjack pays 3:2
            win_amount = self.current_bet * 1.5
            self.message = f"Blackjack! You win ${win_amount:.0f} (3:2 payout)."
            self.player_balance += self.current_bet + win_amount
            self.state = 'RESULTS'
        else:
            self.state = 'PLAYER_TURN'
            self.check_split_option()
            self.message = "Hit, Stand, or Double Down. (Max bet: $1000)"

    def check_split_option(self):
        if len(self.player_hands) < self.current_hand_index:
            return
        """Determines if splitting is possible for the current hand."""
        print(self.player_hands)
        print(self.current_hand_index)
        hand = self.player_hands[self.current_hand_index]
        self.is_split_possible = (len(hand.cards) == 2 and hand.cards[0].rank == hand.cards[1].rank)

    def hit(self):
        """Adds a card to the current player hand."""
        if len(self.player_hands) < self.current_hand_index:
            return
        hand = self.player_hands[self.current_hand_index]
        hand.add_card(self.deck.deal_card())
        
        if hand.calculate_value() > 21:
            self.next_hand_or_dealer_turn()

    def stand(self):
        """Ends the turn for the current player hand."""
        self.next_hand_or_dealer_turn()

    def double_down(self):
        """Doubles the bet, takes one card, and stands."""
        hand = self.player_hands[self.current_hand_index]
        if len(hand.cards) == 2:
            bet_to_add = self.current_bet # Player is doubling the initial bet
            
            if self.player_balance >= bet_to_add:
                self.player_balance -= bet_to_add
                self.current_bet += bet_to_add # Total bet is now double
                hand.add_card(self.deck.deal_card())
                self.next_hand_or_dealer_turn()
            else:
                self.message = "Not enough balance to Double Down."
        else:
            self.message = "Can only Double Down on the first two cards."

    def split(self):
        """Splits the current hand into two new hands."""
        if not self.is_split_possible:
            self.message = "Splitting is not possible."
            return

        original_hand = self.player_hands.pop(self.current_hand_index)
        
        # Create two new hands, each with one card from the original hand
        hand1 = Hand()
        hand1.add_card(original_hand.cards[0])
        hand1.add_card(self.deck.deal_card()) # Second card for first hand

        hand2 = Hand()
        hand2.add_card(original_hand.cards[1])
        hand2.add_card(self.deck.deal_card()) # Second card for second hand

        # Add new hands back to the list
        self.player_hands.insert(self.current_hand_index, hand1)
        self.player_hands.insert(self.current_hand_index + 1, hand2)

        # Update balance for the new bet on the second hand
        self.player_balance -= self.current_bet 

        # Current hand index remains the same (focus on the first of the split hands)
        self.is_split_possible = False
        self.message = f"Hand {self.current_hand_index + 1} of {len(self.player_hands)}: Hit, Stand, or Double Down."


    def next_hand_or_dealer_turn(self):
        """Moves to the next split hand or starts the dealer's turn."""
        self.is_split_possible = False
        self.current_hand_index += 1
        
        if self.current_hand_index < len(self.player_hands):
            # Move to next split hand
            self.message = f"Hand {self.current_hand_index + 1} of {len(self.player_hands)}: Hit, Stand, or Double Down."
            self.check_split_option()
        else:
            # All player hands resolved, move to dealer turn
            self.state = 'DEALER_TURN'
            self.dealer_play()

    def dealer_play(self):
        """Dealer's automated turn: hits on soft 17 (H17 rule)."""
        # Dealer must reveal the hidden card
        dealer_value = self.dealer_hand.calculate_value()

        while dealer_value < 17 or self.dealer_hand.is_soft_17():
            self.dealer_hand.add_card(self.deck.deal_card())
            dealer_value = self.dealer_hand.calculate_value()
        
        self.state = 'RESULTS'
        self.resolve_results()

    def resolve_results(self):
        """Compares player hand(s) to dealer hand and adjusts balance."""
        dealer_value = self.dealer_hand.calculate_value()
        
        final_message = "Hand Results: "
        total_winnings = 0
        
        for i, hand in enumerate(self.player_hands):
            player_value = hand.calculate_value()
            result = ""
            payout = 0

            # 1. Player Bust
            if player_value > 21:
                result = "Bust! Loss."
                payout = 0
            # 2. Player Blackjack (already handled in initial check, but safety here)
            elif player_value == 21 and len(hand.cards) == 2:
                # Should not happen here if initial check is done, but for completeness:
                result = "Blackjack! Win (3:2)."
                payout = self.current_bet * 2.5
            # 3. Dealer Bust
            elif dealer_value > 21:
                result = "Dealer Bust! Win (1:1)."
                payout = self.current_bet * 2
            # 4. Push
            elif player_value == dealer_value:
                result = "Push. Bet returned."
                payout = self.current_bet * 1
            # 5. Player Win
            elif player_value > dealer_value:
                result = "Win (1:1)."
                payout = self.current_bet * 2
            # 6. Player Loss
            else:
                result = "Loss."
                payout = 0

            total_winnings += payout
            final_message += f"[H{i+1}: {result}] "

        self.player_balance += total_winnings
        self.message = final_message
        
        if self.player_balance <= 0 and self.current_bet > 0:
            self.message = "Game Over! You ran out of money."
            self.state = 'GAMEOVER'
        elif self.state != 'GAMEOVER':
            self.message += " Click 'New Hand' to continue."


# --- Drawing Functions ---

def draw_card(surface, card, x, y, is_hidden=False):
    """Draws a single card on the screen."""
    rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
    
    if is_hidden:
        # Draw the back of the card
        pygame.draw.rect(surface, SILVER, rect, border_radius=CARD_BORDER_RADIUS)
        pygame.draw.rect(surface, RED, rect.inflate(-10, -10), border_radius=CARD_BORDER_RADIUS - 5)
        text = font_medium.render("DEALT", True, WHITE)
        surface.blit(text, (x + 15, y + 45))
    else:
        # Draw the front of the card
        pygame.draw.rect(surface, WHITE, rect, border_radius=CARD_BORDER_RADIUS)
        pygame.draw.rect(surface, BLACK, rect, 3, border_radius=CARD_BORDER_RADIUS)
        
        color = RED if card.suit in ('H', 'D') else BLACK
        
        rank_text = font_medium.render(card.rank, True, color)
        suit_text = font_medium.render(card.suit, True, color)
        
        surface.blit(rank_text, (x + 5, y + 5))
        surface.blit(suit_text, (x + 5, y + 90))

def draw_hand(surface, hand, start_x, y, is_player_hand=False, is_active=False):
    """Draws a hand of cards."""
    card_spacing = 20
    
    for i, card in enumerate(hand.cards):
        is_hidden = hand.is_dealer and i == 0 and game.state in ('PLAYER_TURN', 'DEALER_TURN')
        draw_card(surface, card, start_x + i * card_spacing + i * CARD_WIDTH, y, is_hidden)

    # Draw value
    if not hand.is_dealer or game.state in ('RESULTS', 'DEALER_TURN', 'GAMEOVER'):
        value = hand.calculate_value()
        value_text = font_medium.render(f"Value: {value}", True, WHITE)
        surface.blit(value_text, (start_x, y + CARD_HEIGHT + 10))
        
    # Highlight active player hand
    if is_player_hand and is_active and game.state == 'PLAYER_TURN':
        pygame.draw.rect(surface, GOLD, (start_x - 5, y - 5, CARD_WIDTH * len(hand.cards) + CARD_WIDTH + 10, CARD_HEIGHT + 45), 3, border_radius=15)

# Button class for interaction
class Button:
    def __init__(self, text, x, y, w, h, color, text_color=WHITE, action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.action = action
        self.active = True

    def draw(self, surface):
        if not self.active:
            draw_color = (self.color[0]//2, self.color[1]//2, self.color[2]//2) # Greyed out
        else:
            draw_color = self.color
            
        pygame.draw.rect(surface, draw_color, self.rect, border_radius=8)
        
        text_surface = font_medium.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if self.active and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()
                return True
        return False

# --- Game Initialization ---
game = BlackjackGame()

# Button Definitions
def hit_action():
    if game.state == 'PLAYER_TURN':
        game.hit()
        game.check_split_option() # Recalculate if split is possible after hitting first card (if on a split hand)
        
def stand_action():
    if game.state == 'PLAYER_TURN':
        game.stand()

def double_action():
    if game.state == 'PLAYER_TURN':
        game.double_down()

def split_action():
    if game.state == 'PLAYER_TURN' and game.is_split_possible:
        game.split()

def new_hand_action():
    if game.state in ('RESULTS', 'GAMEOVER'):
        game.reset_hand()

def start_hand_action():
    if game.state == 'BETTING':
        try:
            game.bet_amount = int(game.bet_input)
            if 0 < game.bet_amount <= game.player_balance and game.bet_amount <= 1000:
                game.deal()
            elif game.bet_amount > 1000:
                game.message = "Bet cannot exceed $1000."
            elif game.bet_amount <= 0:
                game.message = "Bet must be greater than $0."
            else:
                game.message = "Insufficient balance for this bet."
        except ValueError:
            game.message = "Invalid bet amount."

# Betting input field dimensions
INPUT_W, INPUT_H = 100, 40
INPUT_X = SCREEN_WIDTH - 250
INPUT_Y = 50

# Buttons list
buttons = [
    Button("Hit", 50, SCREEN_HEIGHT - 60, 120, 40, RED, action=hit_action),
    Button("Stand", 200, SCREEN_HEIGHT - 60, 120, 40, GOLD, action=stand_action),
    Button("Double Down", 350, SCREEN_HEIGHT - 60, 150, 40, (0, 150, 255), action=double_action),
    Button("Split", 520, SCREEN_HEIGHT - 60, 120, 40, (50, 50, 50), action=split_action),
    Button("New Hand", SCREEN_WIDTH - 150, SCREEN_HEIGHT - 60, 120, 40, GREEN, action=new_hand_action),
    Button("Place Bet", INPUT_X + INPUT_W + 10, INPUT_Y, 120, 40, BLACK, action=start_hand_action)
]


# --- Main Game Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle button clicks
        for button in buttons:
            button.handle_event(event)

        # Handle betting input
        if game.state == 'BETTING' and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start_hand_action()
            elif event.key == pygame.K_BACKSPACE:
                game.bet_input = game.bet_input[:-1]
            elif event.unicode.isdigit() or (event.unicode == '0' and len(game.bet_input) > 0):
                if len(game.bet_input) < 4: # Max 4 digits for bet
                    game.bet_input += event.unicode
            
            if not game.bet_input:
                game.bet_input = "0"
            game.bet_amount = int(game.bet_input)


    # --- Drawing ---
    screen.fill(GREEN)
    
    # Draw Game Info
    balance_text = font_large.render(f"Balance: ${game.player_balance:.2f}", True, GOLD)
    screen.blit(balance_text, (50, 20))
    
    bet_text = font_medium.render(f"Current Bet: ${game.current_bet:.2f}", True, WHITE)
    screen.blit(bet_text, (50, 70))
    
    msg_text = font_medium.render(game.message, True, WHITE)
    screen.blit(msg_text, (SCREEN_WIDTH // 2 - msg_text.get_width() // 2, 650))

    # --- Betting State UI ---
    if game.state == 'BETTING':
        title_text = font_large.render("PLACE YOUR BET", True, WHITE)
        screen.blit(title_text, (INPUT_X - 100, 10))
        
        # Draw input box
        input_rect = pygame.Rect(INPUT_X, INPUT_Y, INPUT_W, INPUT_H)
        pygame.draw.rect(screen, WHITE, input_rect, border_radius=5)
        pygame.draw.rect(screen, BLACK, input_rect, 2, border_radius=5)
        
        bet_surface = font_medium.render(game.bet_input, True, BLACK)
        screen.blit(bet_surface, (INPUT_X + 5, INPUT_Y + 5))

        # Disable all action buttons, only "Place Bet" is enabled
        for i in range(len(buttons) - 1): # Last button is Place Bet
             buttons[i].active = False
        buttons[-1].active = True
        buttons[-2].active = False # New Hand button

    # --- Game Play UI ---
    else:
        # Dealer Hand (Top of screen)
        dealer_text = font_large.render("DEALER", True, WHITE)
        screen.blit(dealer_text, (50, 120))
        draw_hand(screen, game.dealer_hand, 50, 160)

        # Player Hand(s) (Bottom section)
        player_text = font_large.render("PLAYER HANDS", True, WHITE)
        screen.blit(player_text, (50, 320))

        hand_start_x = 50
        for i, hand in enumerate(game.player_hands):
            is_active = (i == game.current_hand_index)
            # Draw individual hand label for split hands
            if len(game.player_hands) > 1:
                 hand_label = font_medium.render(f"Hand {i+1}", True, GOLD)
                 screen.blit(hand_label, (hand_start_x, 370))

            draw_hand(screen, hand, hand_start_x, 400, is_player_hand=True, is_active=is_active)
            hand_start_x += (len(hand.cards) * CARD_WIDTH + 10) + 50 # Adjust spacing for cards and between hands

        # Enable/Disable Action Buttons based on state and split possibility
        if game.state == 'PLAYER_TURN':
            buttons[0].active = True # Hit
            buttons[1].active = True # Stand
            # Double Down is only available on the first two cards
            buttons[2].active = (len(game.player_hands[game.current_hand_index].cards) == 2)
            # Split is only available on two matching cards
            buttons[3].active = game.is_split_possible
            buttons[4].active = False # New Hand
            buttons[5].active = False # Place Bet
        elif game.state in ('RESULTS', 'GAMEOVER'):
            for i in range(4): buttons[i].active = False
            buttons[4].active = True # New Hand
            buttons[5].active = False # Place Bet
        else: # DEALER_TURN, etc.
             for button in buttons: button.active = False
             
    # Draw all buttons
    for button in buttons:
        button.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
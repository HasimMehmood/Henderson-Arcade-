import pygame 
import random
import os

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CARD_WIDTH, CARD_HEIGHT = 100, 150
CARD_GAP = 20
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 40
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Define the ranks and suits for the deck of cards
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]


# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack")



# Create a font for displaying text
font = pygame.font.Font(None, 36)


deck = [{"rank": rank, "suit": suit, "image": pygame.image.load(f"Assets/Cards/{rank}_of_{suit}.png")} for rank in ranks for suit in suits]
# define shuffle function

def reset_deck():
    global deck
    deck = [{"rank": rank, "suit": suit, "image": pygame.image.load(f"Assets/Cards/{rank}_of_{suit}.png")} for rank in ranks for suit in suits]
    random.shuffle(deck)

reset_deck()


random.shuffle(deck)

player_hand = [deck.pop(), deck.pop()]
dealer_hand = [deck.pop(), deck.pop()]


# Define button coordinates and colors
hit_button_rect = pygame.Rect(20, 500, BUTTON_WIDTH, BUTTON_HEIGHT)
stand_button_rect = pygame.Rect(140, 500, BUTTON_WIDTH, BUTTON_HEIGHT)
new_game_button_rect = pygame.Rect(260, 500, BUTTON_WIDTH, BUTTON_HEIGHT)

# Create a function to display a hand
def display_hand(hand, x, y):
    for card in hand:
        if card:
            screen.blit(card["image"], (x, y))
        x += CARD_WIDTH + CARD_GAP

# Create a function to calculate the value of a hand
def calculate_hand_value(hand):
    value = 0
    num_aces = 0

    for card in hand:
        if card:
            rank = card["rank"]
            if rank in ["Jack", "Queen", "King"]:
                value += 10
            elif rank == "Ace":
                value += 11
                num_aces += 1
            else:
                value += int(rank)

    # Adjust for Aces
    while value > 21 and num_aces > 0:
        value -= 10
        num_aces -= 1

    return value


# Main game loop
running = True
game_over = False
# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # If the user closes the window, exit the game.
        if not game_over :  # Check if the game is not over.
            if calculate_hand_value(player_hand)>= 21: 
                while calculate_hand_value(dealer_hand) < 17:
                    if not deck:
                            reset_deck()  # If the deck is empty, reshuffle the cards.
                    dealer_hand.append(deck.pop())  # Dealer draws a card.
                game_over = True  # The game is now over.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if hit_button_rect.collidepoint(event.pos):
                    # The "Hit" button was clicked, so draw a card and add it to the player's hand.
                    if not deck:
                        reset_deck()  # If the deck is empty, reshuffle the cards.
                    player_hand.append(deck.pop())  # Draw a card from the deck.
                elif stand_button_rect.collidepoint(event.pos):
                    # The "Stand" button was clicked, so the player's turn is over. Or the value is over 21.
                    # The dealer will now draw cards until their hand value is at least 17.
                    while calculate_hand_value(dealer_hand) < 17:
                        if not deck:
                            reset_deck()  # If the deck is empty, reshuffle the cards.
                        dealer_hand.append(deck.pop())  # Dealer draws a card.
                    game_over = True  # The game is now over.

        if event.type == pygame.MOUSEBUTTONDOWN:
            if new_game_button_rect.collidepoint(event.pos):
                # The "New Game" button was clicked, so reset the game by reshuffling the deck
                # and dealing new hands for both the player and the dealer.
                reset_deck()  # If the deck is empty, reshuffle the cards.
                player_hand = [deck.pop(), deck.pop()]  # Deal two cards to the player.
                dealer_hand = [deck.pop(), deck.pop()]  # Deal two cards to the dealer.
                game_over = False  # The game is not over.


    screen.fill(WHITE)

    # Display player's hand
    screen.blit(font.render("Player's Hand:", True, RED), (20, 20))
    display_hand(player_hand, 20, 60)
    player_value = calculate_hand_value(player_hand)
    screen.blit(font.render(f"Player's Hand Value: {player_value}", True, RED), (20, 250))

    # Display dealer's hand (showing only one card if the game is not over)
    # Display dealer's hand (showing the entire hand)
    screen.blit(font.render("Dealer's Hand:", True, RED), (20, 300))
    display_hand(dealer_hand, 20, 340)


    if game_over:
        dealer_value = calculate_hand_value(dealer_hand)
        screen.blit(font.render(f"Dealer's Hand Value: {dealer_value}", True, RED), (20, 470))

    # Create buttons
    pygame.draw.rect(screen, RED, hit_button_rect)
    pygame.draw.rect(screen, RED, stand_button_rect)
    pygame.draw.rect(screen, RED, new_game_button_rect)
    screen.blit(font.render("Hit", True, WHITE), (30, 505))
    screen.blit(font.render("Stand", True, WHITE), (150, 505))
    screen.blit(font.render("New Game", True, WHITE), (270, 505))

    # Check for win/lose conditions
    if game_over:
        if player_value > 21:
            screen.blit(font.render("Player busts! Dealer wins.", True, RED), (300, 250))
        elif dealer_value > 21:
            screen.blit(font.render("Dealer busts! Player wins.", True, RED), (300, 250))
        elif dealer_value > player_value:
            screen.blit(font.render("Dealer wins.", True, RED), (300, 250))
        elif dealer_value < player_value:
            screen.blit(font.render("Player wins.", True, RED), (300, 250))
        else:
            screen.blit(font.render("It's a tie!", True, RED), (300, 250))

    pygame.display.flip()

pygame.quit()

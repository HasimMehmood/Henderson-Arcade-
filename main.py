# Example file showing a basic pygame "game loop"
import pygame
import pygame
import random

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CARD_WIDTH, CARD_HEIGHT = 100, 150
CARD_GAP = 20
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack")

# Load card images (image card files)
# Example image filenames: "2_of_hearts.png", "ace_of_spades.png", etc.
# Replace these with the card images.
card_images = [pygame.image.load(f"{rank}_of_{suit}.png") for rank in ranks for suit in suits]

# Create a font for displaying text
font = pygame.font.Font(None, 36)

# Define the deck of cards and hands
deck = [{"rank": rank, "suit": suit, "image": image} for rank, suit, image in zip(ranks, suits, card_images)]
random.shuffle(deck)
player_hand = [deck.pop(), deck.pop()]
dealer_hand = [deck.pop(), deck.pop()]

# Create a function to display a hand
def display_hand(hand, x, y):
    for card in hand:
        screen.blit(card["image"], (x, y))
        x += CARD_WIDTH + CARD_GAP

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    # Display player's hand
    screen.blit(font.render("Player's Hand:", True, RED), (20, 20))
    display_hand(player_hand, 20, 60)

    # Display dealer's hand (showing only one card)
    screen.blit(font.render("Dealer's Hand:", True, RED), (20, 300))
    display_hand([dealer_hand[0]] + [None] * (len(dealer_hand) - 1), 20, 340)

    pygame.display.flip()

pygame.quit()


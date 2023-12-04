import pygame 
import random 
from PIL import Image, ImageSequence

# Initialize Pygame
pygame.init()

#Set Game icon
pygame.display.set_icon(pygame.image.load("Assets\Favicon\BlackJack_32x32.png") )

# Define constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CARD_WIDTH, CARD_HEIGHT = 100, 150
CARD_GAP = 20
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 40
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK= (0,0,0)
Money= 100
hit_button= pygame.image.load("Assets\\Buttons\\Button/Hit_Button.png")
stand_button= pygame.image.load("Assets\\Buttons\\Button/Stand_Button.png")
new_game_button= pygame.image.load("Assets\\Buttons\\Button/NewGame_Button.png")
bet_button= pygame.image.load("Assets\\Betting\\Bet_Button.png")
left_button= pygame.image.load("Assets\\Betting\Left_Button.png")
right_button= pygame.image.load("Assets\\Betting\\Right_Button.png")
UI_betting= pygame.image.load("Assets\\Betting\\UI Betting.png")
coin_pile= pygame.image.load("Assets\\Betting\\Coin_Pile.png")
play_button= pygame.image.load("Assets\\Start Screen\\Play_Button.png")
back_of_card= pygame.image.load("Assets\\Cards\\Back_of_Card.png")
start_screen= pygame.image.load("Assets\\Start Screen\\Start_Screen.png")
animations = ["New Game", "Hit", "Stand", "Play Button", "Bet Button", "Left Button", "Right Button"]
# Define the ranks and suits for the deck of cards
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]

# Create a dictionary to store animation frames
animation_frames = {}

# Load animations using Pillow and store frames in the dictionary
for animation_name in animations:
    animation_path = f"Assets/Buttons/Click Animation/{animation_name}.gif"
    animation = Image.open(animation_path)
    frames = [frame.copy().convert('RGB') for frame in ImageSequence.Iterator(animation)]
    animation_frames[animation_name] = frames
    animation_width, animation_height = animation_frames[animation_name][0].size # Get the size of the first frame to determine the dimensions

def play_anim(anim_name, xcoord, ycoord):
    for frame in animation_frames[anim_name]:
        pygame_frame = pygame.image.fromstring(frame.tobytes(), frame.size, 'RGB')
        screen.blit(pygame_frame, (xcoord, ycoord))
        pygame.display.flip()
        pygame.time.delay(25)  # Adjust the delay between frames as needed

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack")

# Create a font for displaying text
font = pygame.font.Font(None, 36)

# define shuffle function, it will define the deck array
def reset_deck():
    global deck
    deck = [{"rank": rank, "suit": suit, "image": pygame.image.load(f"Assets/Cards/{rank}_of_{suit}.png")} for rank in ranks for suit in suits]
    random.shuffle(deck)

reset_deck()


random.shuffle(deck)

player_hand = [deck.pop(), deck.pop()]
dealer_hand = [deck.pop(), deck.pop()]


# Define button coordinates and colors
hit_button_rect = pygame.Rect(20, 520, BUTTON_WIDTH, BUTTON_HEIGHT)
stand_button_rect = pygame.Rect(140, 520, BUTTON_WIDTH, BUTTON_HEIGHT)
new_game_button_rect = pygame.Rect(260, 520, BUTTON_WIDTH, BUTTON_HEIGHT)
play_button_rect= pygame.Rect(520,480, 240, 124)
UI_betting_rect= pygame.Rect(400,100, 350,300)
coin_pile_rect= pygame.Rect(UI_betting_rect.left+230, UI_betting_rect.top+30, 82,87)
bet_button_rect= pygame.Rect(UI_betting_rect.left+100, UI_betting_rect.top+200, 145, 60)
left_button_rect= pygame.Rect(bet_button_rect.left+104,bet_button_rect.top-40, 35,35)
right_button_rect=pygame.Rect(left_button_rect.left-100 ,left_button_rect.top, 35,35)

# Create a function to display a hand
def display_hand(hand, x, y):
    for card in hand:
        if card:
            screen.blit(card["image"], (x, y))
        x += CARD_WIDTH + CARD_GAP

def display_dealer_card(x, y):
    for card in dealer_hand[:1]:
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


    #Create function to Draw cards for dealer
def dealer_draw():
    while calculate_hand_value(dealer_hand) < 17:
        if not deck:
            reset_deck()  # If the deck is empty, reshuffle the cards.
        dealer_hand.append(deck.pop())  # Dealer draws a card.



# Main game loop
running = True
game_over = False
game_start=False
bet_placed= False
bet=0
money=0

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # If the user closes the window, exit the game.
    if game_start == False: 
        screen.blit(start_screen, (0,0))
        screen.blit(play_button, play_button_rect)
        if(event.type== pygame.MOUSEBUTTONDOWN and play_button_rect.collidepoint(event.pos)):
            play_anim("Play Button", play_button_rect.left, play_button_rect.top )
            game_start=True
    else: 
        if not game_over :  # Check if the game is not over.
            if calculate_hand_value(player_hand)>= 21:  
                dealer_draw()
                game_over = True  # The game is now over. 
            elif (event.type == pygame.MOUSEBUTTONDOWN and bet_placed==False): 
                if left_button_rect.collidepoint(event.pos):
                    print("Left button clicked")
                    bet= bet-10
                    print(bet)
                    play_anim("Left Button", left_button_rect.left, left_button_rect.top)
                elif right_button_rect.collidepoint(event.pos):
                    print("Right button clicked")
                    play_anim("Right Button", right_button_rect.left, right_button_rect.top)
                    bet= bet+10
                    print(bet)
                elif bet_button_rect.collidepoint(event.pos):
                    print("Bet button pressed")
                    play_anim("Bet Button", bet_button_rect.left, bet_button_rect.top)
                    bet_placed=True
                   
            elif (event.type == pygame.MOUSEBUTTONDOWN and bet_placed==True):
                if hit_button_rect.collidepoint(event.pos):
                    # The "Hit" button was clicked, so draw a card and add it to the player's hand.
                    play_anim("Hit", hit_button_rect.left, hit_button_rect.top)
                    player_hand.append(deck.pop())  # Draw a card from the deck.
                elif stand_button_rect.collidepoint(event.pos):
                    # The "Stand" button was clicked, so the player's turn is over. Or the value is over 21.
                    play_anim("Stand", stand_button_rect.left,stand_button_rect.top)
                    dealer_draw()
                    game_over = True  # The game is now over.
                    bet_placed=False
                    
     
        if event.type == pygame.MOUSEBUTTONDOWN:
            if new_game_button_rect.collidepoint(event.pos):
                # The "New Game" button was clicked, so reset the game by reshuffling the deck
                # and dealing new hands for both the player and the dealer.
                play_anim("New Game", new_game_button_rect.left,new_game_button_rect.top)
                pygame.display.flip()
                pygame.time.delay(50)  # Display the animation for 1000 milliseconds (adjust as needed)
                reset_deck()  # If the deck is empty, reshuffle the cards.
                player_hand = [deck.pop(), deck.pop()]  # Deal two cards to the player.
                dealer_hand = [deck.pop(), deck.pop()]  # Deal two cards to the dealer.
                game_over = False  # The game is not over.
                bet_placed=False

        screen.fill(WHITE)

        # Display player's hand
        screen.blit(font.render("Player's Hand:", True, BLACK), (20, 20))
        display_hand(player_hand, 20, 60)
        player_value = calculate_hand_value(player_hand)
        screen.blit(font.render(f"Player's Hand Value: {player_value}", True, BLACK), (20, 250))



        # Display dealer's hand text
        screen.blit(font.render("Dealer's Hand:", True, BLACK), (20, 300))

        # Show the dealer's first card face-down during the player's turn
        if not game_over:
            screen.blit(back_of_card, (140, 340))
            display_dealer_card(20, 340 )
        else:
            display_hand(dealer_hand, 20, 340)  # Show the entire dealer's hand

        if game_over:
            dealer_value = calculate_hand_value(dealer_hand)
            screen.blit(font.render(f"Dealer's Hand Value: {dealer_value}", True, BLACK), (20, 500))

        # Create buttons
        screen.blit(hit_button, hit_button_rect)
        screen.blit(stand_button, stand_button_rect)
        screen.blit(new_game_button, new_game_button_rect)
        screen.blit(UI_betting,UI_betting_rect)
        screen.blit(coin_pile, coin_pile_rect)
        screen.blit(bet_button, bet_button_rect)
        screen.blit(left_button,left_button_rect)
        screen.blit(right_button, right_button_rect)       

        # Check for win/lose conditions
        if game_over:
            if player_value > 21:
                screen.blit(font.render(" Player busts! Dealer wins.", True, BLACK), (300, 250))
                money= money+bet
            elif dealer_value > 21:
                screen.blit(font.render(" Dealer busts! Player wins.", True, BLACK), (300, 250))
                money= money-bet
            elif dealer_value > player_value:
                screen.blit(font.render(" Dealer wins.", True, BLACK), (300, 250))
                money= money-bet
            elif dealer_value < player_value:
                screen.blit(font.render(" Player wins.", True, BLACK), (300, 250))
                money= money+bet
            else:
                screen.blit(font.render(" It's a tie!", True, BLACK), (300, 250))

    pygame.display.flip()

pygame.quit()

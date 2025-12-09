# black jack in python with pygame
# =========================
# 1. Importeren van modules
# =========================
import copy
import random
import pygame
import os     # voor padbewerkingen, kaarten map
import re     # voor parsen van kaartnamen

pygame.init()

# =========================
# 2. Game variabelen
# =========================
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4
WIDTH = 600
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Pygame Blackjack!")
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)
active = False
# win, loss, draw/push
records = [0, 0, 0]
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
outcome = 0
add_score = False
results = ['', 'PLAYER BUSTED o_O', 'Player WINS! :)', 'DEALER WINS :(', 'TIE GAME...']
# startmenu variabelen
menu_active = True
start_buttons = []




# =========================
# 3. Kaartafbeeldingen (NIEUW)
# =========================
CARD_SIZE = (120, 220)  # grootte van kaarten
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'png')  # map met png's
rank_to_surfaces_master = {}   # masterlijst van alle afbeeldingen per rank
rank_to_surfaces_pool = {}     # pool die we leegtrekken bij dealen
card_back_surface = None       # achterkant van kaart
my_hand_images = []            # afbeeldingen van spelerhand
dealer_hand_images = []        # afbeeldingen van dealerhand





def draw_start_menu():
    global start_buttons
    start_buttons = []

    screen.fill('black')
    # Titel
    title_text = font.render("BLACKJACK", True, 'white')
    # Plaats het in het midden van het scherm: WIDTH//2 is het midden van het scherm
    # We trekken de helft van de breedte van de tekst af om precies te centreren
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 200))




# =========================
# 4. Rank parser (NIEUW)
# =========================
SUIT_TOKENS = r"hearts|heart|diamonds|diamond|clubs|club|spades|spade|h|d|c|s"

def parse_rank_from_filename(name_lower):
    base = re.sub(r"[_\-]+", " ", name_lower)  # normalize separators
    if 'joker' in base:
        return None
    if re.search(r"\b10\b", base):
        return '10'
    m = re.search(r"\b([2-9])\b", base)
    if m:
        return m.group(1)
    for word, rank in [(r"\bace\b", 'A'), (r"\bking\b", 'K'), (r"\bqueen\b", 'Q'), (r"\bjack\b", 'J')]:
        if re.search(word, base):
            return rank
    for letter, rank in [(r"\bA\b", 'A'), (r"\bK\b", 'K'), (r"\bQ\b", 'Q'), (r"\bJ\b", 'J')]:
        if re.search(letter, name_lower, flags=re.IGNORECASE):
            if re.search(rf"\b({SUIT_TOKENS})\b", base):
                return rank
    return None

# =========================
# 5. Load card images (NIEUW)
# =========================

def load_card_assets(folder, size):
    global card_back_surface, rank_to_surfaces_master
    if not os.path.isdir(folder):
        return
    backs = []
    rank_map = {r: [] for r in cards}
    for filename in os.listdir(folder):
        if not filename.lower().endswith('.png'):
            continue
        lower = filename.lower()
        if 'joker' in lower:
            continue
        full_path = os.path.join(folder, filename)
        try:
            image = pygame.image.load(full_path).convert_alpha()
            image = pygame.transform.smoothscale(image, size)
        except:
            continue
        if 'back' in lower or 'background' in lower:
            backs.append(image)
            continue
        rank = parse_rank_from_filename(lower)
        if rank:
            rank_map[rank].append(image)
    card_back_surface = backs[0] if backs else None
    rank_to_surfaces_master = rank_map    


# =========================
# 6. Reset image pool (NIEUW)
# =========================
def reset_image_pool():
    global rank_to_surfaces_pool, my_hand_images, dealer_hand_images
    rank_to_surfaces_pool = {r:list(surfaces) for r, surfaces in rank_to_surfaces_master.items()}
    my_hand_images = []
    dealer_hand_images = []



# =========================
# 7. Choose surface for rank (NIEUW)
# =========================
def choose_surface_for_rank(rank):
    pool = rank_to_surfaces_pool.get(rank, [])
    if pool:
        return pool.pop()
    master = rank_to_surfaces_master.get(rank, [])
    return master[-1] if master else None



# =========================
# 8. Deal cards (Aangepast)
# =========================
def deal_cards(current_hand, current_deck, image_list):
    card_index = random.randint(0,len(current_deck)-1)
    rank = current_deck[card_index]
    current_hand.append(rank)
    current_deck.pop(card_index)
    surf = choose_surface_for_rank(rank)  # nieuwe code: afbeelding koppelen
    image_list.append(surf)
    return current_hand, current_deck



# =========================
# 9. Draw cards (Aangepast)
# =========================

# draw cards visually onto screen
def draw_cards(player, dealer, reveal):
    # speler kaarten
    for i in range(len(player)):
        x = 70 + (70*i)
        y = 460 + (5*i)
        rect = pygame.Rect(x, y, CARD_SIZE[0], CARD_SIZE[1])
        pygame.draw.rect(screen, 'white', rect, 0, 5)
        pygame.draw.rect(screen, 'red', rect, 3, 5)
        surf = my_hand_images[i] if i < len(my_hand_images) else None
        if surf:
            screen.blit(surf, (x, y))
        else:
            screen.blit(font.render(str(player[i]), True, 'black'), (x+10, y+10))
    # dealer kaarten
    for i in range(len(dealer)):
        x = 70 + (70*i)
        y = 160 + (5*i)
        rect = pygame.Rect(x, y, CARD_SIZE[0], CARD_SIZE[1])
        pygame.draw.rect(screen, 'white', rect, 0, 5)
        pygame.draw.rect(screen, 'red', rect, 3, 5)
        if i == 0 and not reveal and card_back_surface:
            screen.blit(card_back_surface, (x, y))
        else:
            surf = dealer_hand_images[i] if i < len(dealer_hand_images) else None
            if surf:
                screen.blit(surf, (x, y))
            else:
                screen.blit(font.render(str(dealer[i]) if (i != 0 or reveal) else '???', True, 'black'), (x+10, y+10))
        

# pass in player or dealer hand and get best score possible
def calculate_score(hand):
    # calculate hand score fresh each time, check how many aces we have
    hand_score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
        # for 2, 3, 4, 5, 6, 7, 8, 9 - just add the number to total
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])
        # for 10, J, Q, K - add 10 to total
        if hand[i] in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        # for aces, start by adding 11, we'll check laterif we need to reduce it to 1.
        elif hand[i] == 'A':
            hand_score += 11
    # determine how many aces need to be 1 instead of 11 to get under 21 if possible
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score



# draw game conditions and buttons 
def draw_game(act, record, result):
    button_list = []
    # initially on startup (not active) only option is to deal new hand
    if not act:
        deal = pygame.draw.rect(screen, 'white', [150, 20, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 20, 300, 100], 3, 5)
        deal_text = font.render('DEAL HAND', True, 'black')
        screen.blit(deal_text, (165, 50))
        button_list.append(deal)
    
    # once game started, show hit and stand buttons and win/loss records
    else:
        hit = pygame.draw.rect(screen, 'white', [0, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [0, 700, 300, 100], 3, 5)
        hit_text = font.render('HIT ME', True, 'black')
        screen.blit(hit_text, (55, 735))
        button_list.append(hit)
        stand = pygame.draw.rect(screen, 'white', [300, 700, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [300, 700, 300, 100], 3, 5)
        stand_text = font.render('STAND', True, 'black')
        screen.blit(stand_text, (355, 735))
        button_list.append(stand)
        score_text = smaller_font.render(f"Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}", True, 'white')
        screen.blit(score_text, (15, 840))
    # if there is an outcome for the hand that was played, display a restart button and tell user what happened
    if result != 0:
        screen.blit(font.render(results[result], True, 'white'), (15, 25))
        deal = pygame.draw.rect(screen, 'white', [150, 220, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 220, 300, 100], 3, 5)
        pygame.draw.rect(screen, 'black', [153, 223, 294, 94], 3, 5)
        deal_text = font.render('NEW HAND', True, 'black')
        screen.blit(deal_text, (165, 250))
        button_list.append(deal)
    return button_list


    


# draw scores for player and dealer on screen
def draw_scores(player, dealer):
    screen.blit(font.render(f"Score[{player}]", True, 'white'), (350, 400))
    if reveal_dealer:
        screen.blit(font.render(f"Score[{dealer}]", True, 'white'), (350, 100))


# check endgame conditions function
def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    # check end game scenarios is player has stood, busted or blackjacked
    # result 1- player bust, 2-win, 3-loss, 4-push
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4
        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1
            add = False
    return result, totals, add



# main game loop
run = True
load_card_assets(ASSETS_DIR, CARD_SIZE) # nieuw: laad alle kaarten

while run:
    # run game at our framerate an fill screen with bg color
    timer.tick(fps)
    screen.fill('black')
    # initial deal to player and dealer
    if initial_deal:
        reset_image_pool()  # nieuw: reset de afbeelding pool
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck, my_hand_images)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck, dealer_hand_images)
        print(my_hand, dealer_hand)
        initial_deal = False
    # once game is activated, and dealt, calculate scores and display cards
    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck, dealer_hand_images)
        draw_scores(player_score, dealer_score)

    buttons = draw_game(active, records, outcome)


    # event handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    reveal_dealer = False
                    outcome = 0
                    add_score = True
            else:
                # if player can hit, allow them to draw a card
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck, my_hand_images)

                 # allow player to end turn (stand)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        outcome = 0
                        add_score = True
                        dealer_score = 0
                        player_score = 0

    # if player busts, automatically end turn - treat like a stand 
    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True 
    
    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)

                

    pygame.display.flip()

pygame.quit()





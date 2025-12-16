# black jack in python with pygame
# =========================
# 1. Importeren van modules
# =========================
import copy
import random
import pygame
import os     # voor padbewerkingen, kaarten map
import re     # voor parsen van kaartnamen
import math   # voor wiskundige functies


pygame.init()
pygame.mixer.init()

# =========================
# 2. Game variabelen
# =========================
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4
WIDTH = 800
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Pygame Blackjack!")
fps = 60
timer = pygame.time.Clock()


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

# =========================
card_animations = []
chip_particles = []
button_hover = [False, False, False]
glow_timer = 0
win_celebration = 0
pulse_timer = 0

GREEN_FELT = (0, 100, 0)
DARK_GREEN = (0, 70, 0)
GOLD = (255, 215, 0)
DARK_GOLD = (184, 134, 11)
RED = (220, 20, 60)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

card_font = pygame.font.Font('freesansbold.ttf', 48)
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)
tiny_font = pygame.font.Font('freesansbold.ttf', 24)


menu_active = True
start_buttons = []
win_sound_played = False
lose_sound_played = False
# =========================







CARD_SIZE = (100, 140)  # grootte van kaarten
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'png')  # map met png's
rank_to_surfaces_master = {}   # masterlijst van alle afbeeldingen per rank
rank_to_surfaces_pool = {}     # pool die we leegtrekken bij dealen
card_back_surface = None       # achterkant van kaart
my_hand_images = []            # afbeeldingen van spelerhand
dealer_hand_images = []        # afbeeldingen van dealerhand



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

def reset_image_pool():
    global rank_to_surfaces_pool, my_hand_images, dealer_hand_images
    rank_to_surfaces_pool = {r:list(surfaces) for r, surfaces in rank_to_surfaces_master.items()}
    my_hand_images = []
    dealer_hand_images = []

def choose_surface_for_rank(rank):
    pool = rank_to_surfaces_pool.get(rank, [])
    if pool:
        return pool.pop()
    master = rank_to_surfaces_master.get(rank, [])
    return master[-1] if master else None

def deal_cards(current_hand, current_deck, image_list):
    card_index = random.randint(0,len(current_deck)-1)
    rank = current_deck[card_index]
    current_hand.append(rank)
    current_deck.pop(card_index)
    surf = choose_surface_for_rank(rank)  # nieuwe code: afbeelding koppelen
    image_list.append(surf)
    return current_hand, current_deck

# draw cards visually onto screen
def draw_cards(player, dealer, reveal):
     # NIEUW: DEALER LABEL (uit jouw mooie versie)
    dealer_label = tiny_font.render("DEALER", True, GOLD)
    screen.blit(dealer_label, (50, 30))

     # NIEUW: PLAYER LABEL (uit jouw mooie versie)
    player_label = tiny_font.render("PLAYER", True, GOLD)
    screen.blit(player_label, (50, 480))

    # speler kaarten
    for i in range(len(player)):
        x = 50 + (120 * i)  # 120 pixels tussen (zoals mooie versie)
        y = 510
        rect = pygame.Rect(x, y, CARD_SIZE[0], CARD_SIZE[1])
        # NIEUW: Schaduw effect (5 pixels rechts en onder)
        shadow_rect = pygame.Rect(x + 5, y + 5, CARD_SIZE[0], CARD_SIZE[1])
        pygame.draw.rect(screen, (30, 30, 30), shadow_rect, 0, 10)

        # NIEUW: Kaart met rondere hoeken
        pygame.draw.rect(screen, WHITE, rect, 0, 10)

        # NIEUW: Gouden rand
        pygame.draw.rect(screen, GOLD, rect, 3, 10)

        surf = my_hand_images[i] if i < len(my_hand_images) else None
        if surf:
            screen.blit(surf, (x, y))
        else:
            screen.blit(font.render(str(player[i]), True, 'black'), (x+10, y+10))
    # dealer kaarten
    for i in range(len(dealer)):
        x = 50 + (120 * i)  # 120 pixels tussen (zoals mooie versie)
        y = 60
        rect = pygame.Rect(x, y, CARD_SIZE[0], CARD_SIZE[1])
        # Schaduw
        shadow_rect = pygame.Rect(x + 5, y + 5, CARD_SIZE[0], CARD_SIZE[1])
        pygame.draw.rect(screen, (30, 30, 30), shadow_rect, 0, 10)
        # kaart
        pygame.draw.rect(screen, 'white', rect, 0, 10)
        pygame.draw.rect(screen, 'gold', rect, 3, 10)

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
    global button_hover, win_celebration, chip_particles, win_sound_played, lose_sound_played


    # RESET sound_played als result naar 0 gaat
    # (voeg dit toe aan het BEGIN van draw_game())
    if result == 0:
        win_sound_played = False
        lose_sound_played = False

    # NIEUW: Haal de muispositie op
    mouse_pos = pygame.mouse.get_pos()

    # ========================================
    # DEEL A: WIN CELEBRATION PARTICLES
    # ========================================
    # Als win_celebration > 0, dan is er een FEESTJE bezig!
    if win_celebration > 0:
        # Voor ELKE FRAME dat er feest is:
        # Maak 3 NIEUWE particles (chips)
        for _ in range(3):
            # Particle parameters:
            # x = random tussen 0 en 800 (ergens bovenaan scherm)
            # y = 0 (HELEMAAL bovenaan)
            # color = random: GOLD, RED of WHITE
            chip_particles.append(Particle(
                random.randint(0, WIDTH),  # Random x positie
                0,                         # y = 0 (bovenkant)
                random.choice([GOLD, RED, WHITE])  # Random kleur
            ))
        
        # Verminder de feest-timer met 1
        win_celebration -= 1
        # Voorbeeld: was 60 → nu 59 → volgende frame 58 → ... → 0


    # ========================================
    # DEEL B: UPDATE ALLE PARTICLES
    # ========================================
    # Loop door ALLE particles die er zijn
    # [:] maakt een KOPIE van de lijst (anders crasht het als we verwijderen)
    for particle in chip_particles[:]:
        # 1. Update de particle (beweeg, zwaartekracht, etc.)
        particle.update()
        
        # 2. Check of particle "dood" is (life <= 0)
        if particle.life <= 0:
            # Verwijder uit de lijst (doe het muntstuk weg)
            chip_particles.remove(particle)
        else:
            # 3. Als particle nog leeft: TEKEN het
            particle.draw(screen)



    # initially on startup (not active) only option is to deal new hand
    if not act:
        # NIEUW: Maak een pygame.Rect object
        deal = pygame.Rect(250, 400, 300, 100)
        
        # NIEUW: Check of muis over knop zweeft
        button_hover[0] = deal.collidepoint(mouse_pos)
        
        # NIEUW: Gebruik de glow button functie!
        # GREEN_FELT = achtergrond, GOLD = glow kleur
        draw_glow_button(deal, 'DEAL HAND', GREEN_FELT, GOLD, button_hover[0])
        
        button_list.append(deal)
    
    # once game started, show hit and stand buttons and win/loss records
    else:
        # HIT knop - groene achtergrond
        hit = pygame.Rect(100, 750, 240, 80)
        button_hover[0] = hit.collidepoint(mouse_pos)
        draw_glow_button(hit, 'HIT ME', GREEN_FELT, GOLD, button_hover[0])
        button_list.append(hit)
        
        # STAND knop - RODE achtergrond (voor contrast)
        stand = pygame.Rect(460, 750, 240, 80)
        button_hover[1] = stand.collidepoint(mouse_pos)
        draw_glow_button(stand, 'STAND', RED, GOLD, button_hover[1])  # RED i.p.v. GREEN_FELT
        button_list.append(stand)

        # Maak een mooie panel voor de statistieken
        panel_rect = pygame.Rect(50, 840, WIDTH - 100, 50)  # Breed, dunne panel

        # Transparante zwarte achtergrond
        s = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(s, (0, 0, 0, 150), s.get_rect(), border_radius=10)
        screen.blit(s, panel_rect.topleft)

        # Gouden rand
        pygame.draw.rect(screen, GOLD, panel_rect, 2, 10)

        # Tekst gecentreerd in de panel
        score_text = tiny_font.render(f"Wins: {record[0]}  Losses: {record[1]}  Draws: {record[2]}", 
                                     True, GOLD)
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 855))



    # if there is an outcome for the hand that was played, display a restart button and tell user what happened
    if result != 0:
        # Result banner - Dit maakt de mooie "Player WINS!" banner
    
        # 1. Bepaal kleuren voor elk resultaat type
        #    Dit is een dictionary: {key: value}
        #    key=result_nummer, value=kleur
        result_colors = {1: RED, 2: GOLD, 3: RED, 4: WHITE}
        # 1 = PLAYER BUSTED → Rood
        # 2 = Player WINS! → Goud (feest!)
        # 3 = DEALER WINS → Rood  
        # 4 = TIE GAME... → Wit

        # 2. Bereken Y-positie met animatie
        #    pulse_timer gaat elke frame omhoog (in main loop)
        #    math.sin() geeft een golf tussen -1 en 1
        #    Dus banner_y gaat: 275 → 280 → 285 → 280 → 275...
        banner_y = 280 + int(5 * math.sin(pulse_timer / 10))
        # Start op 280 pixels van boven
        # +/- 5 pixels beweging
        # /10 = langzame beweging (elke 10 frames een cyclus)

        # 3. Maak de tekst surface
        #    results[result] = de juiste tekst uit de results lijst
        #    result_colors.get(result, WHITE) = haal kleur op, anders wit
        result_surf = font.render(results[result], True, result_colors.get(result, WHITE))

        # 4. Centreer de tekst op scherm
        #    result_rect wordt een rechthoek ROND de tekst
        #    center=(WIDTH//2, banner_y) = midden van scherm, op banner_y hoogte
        result_rect = result_surf.get_rect(center=(WIDTH // 2, banner_y))

        # 5. Maak een grotere rechthoek voor de banner achtergrond
        #    result_rect.x - 20 = 20 pixels links van tekst beginnen
        #    result_rect.y - 10 = 10 pixels boven tekst beginnen  
        #    result_rect.width + 40 = 20+20 pixels breder dan tekst
        #    result_rect.height + 20 = 10+10 pixels hoger dan tekst
        bg_rect = pygame.Rect(result_rect.x - 20, result_rect.y - 10, 
                              result_rect.width + 40, result_rect.height + 20)
        
        # 6. Maak transparante banner achtergrond
        #    pygame.SRCALPHA = maak een doorzichtig canvas
        s = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)

        # 7. Teken zwarte rechthoek op transparant canvas
        #    (0, 0, 0, 200) = zwart met 200/255 transparantie (78% zichtbaar)
        #    border_radius=10 = maak hoeken rond
        pygame.draw.rect(s, (0, 0, 0, 200), s.get_rect(), border_radius=10)

        # 8. Plak het transparante canvas op het scherm
        #    bg_rect.topleft = linkerbovenhoek van banner
        screen.blit(s, bg_rect.topleft)

        # 9. Teken een rand OM de banner
        #    result_colors.get(result, WHITE) = rand in resultaat kleur
        #    3 = dikte van de rand (3 pixels)
        pygame.draw.rect(screen, result_colors.get(result, WHITE), bg_rect, 3, 10)

        # 10. Teken de tekst over de banner heen
        screen.blit(result_surf, result_rect)

        # 11. NEW HAND knop (voor nieuwe ronde)
        #     250, 340 = positie (x, y)
        #     300, 80 = grootte (breedte, hoogte)
        deal = pygame.Rect(250, 340, 300, 80)


        # 12. Check of muis over knop zweeft
        button_hover[2] = deal.collidepoint(mouse_pos)

        # 13. Teken de knop met glow effect
        draw_glow_button(deal, 'NEW HAND', GREEN_FELT, GOLD, button_hover[2])

        # 14. Voeg toe aan button lijst voor klik detectie
        button_list.append(deal)

        # NIEUW TOEVOEGEN: Start feest bij WIN
        if result == 2:  # result=2 betekent "PLAYER WINS"
        # max(huidige_timer, 60) = kies de GROOTSTE
        # Voorbeeld 1: win_celebration was 0 → max(0, 60) = 60
        # Voorbeeld 2: win_celebration was 30 → max(30, 60) = 60
        # Voorbeeld 3: win_celebration was 90 → max(90, 60) = 90
            win_celebration = max(win_celebration, 60)
        # Dit betekent: "Zorg dat feest MINSTENS 60 frames duurt"
        # WIN GELUID - maar 1x
        if result == 2 and not win_sound_played:
            try:
                pygame.mixer.Sound("Sounds\level-up-05-326133.mp3").play()
                win_sound_played = True  # Nu nooit meer dit spel
            except:
                pass

        if (result == 1 or result == 3) and not lose_sound_played:
            try:
                pygame.mixer.Sound("Sounds/falled-sound-effect-278635.mp3").play()
                lose_sound_played = True
            except:
                pass

            

        
    return button_list



# draw scores for player and dealer on screen
def draw_scores(player, dealer):
    # Player score panel (altijd zichtbaar)
    player_panel = pygame.Rect(50, 680, 220, 50)  # Positie aanpassen aan jouw layout
    pygame.draw.rect(screen, (0, 0, 0, 180), player_panel, border_radius=10)
    pygame.draw.rect(screen, GOLD, player_panel, 3, 10)

    player_text = smaller_font.render(f"Score: {player}", True, GOLD)
    screen.blit(player_text, (player_panel.centerx - player_text.get_width()//2, 
                              player_panel.centery - player_text.get_height()//2))
    
    # Dealer score (alleen als onthuld)
    if reveal_dealer:
        dealer_panel = pygame.Rect(50, 230, 220, 50)
        pygame.draw.rect(screen, (0, 0, 0, 180), dealer_panel, border_radius=10)
        pygame.draw.rect(screen, GOLD, dealer_panel, 3, 10)
        
        dealer_text = smaller_font.render(f"Score: {dealer}", True, GOLD)
        screen.blit(dealer_text, (dealer_panel.centerx - dealer_text.get_width()//2,
                                 dealer_panel.centery - dealer_text.get_height()//2))

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


def draw_gradient_bg():
    """
    Teken een gradient achtergrond van donker groen bovenaan naar licht groen onderaan.
    We tekenen 900 horizontale lijnen (één per pixel rij), elk met een iets andere kleur.
    """
    # Ons scherm is HEIGHT pixels hoog (HEIGHT = 900)
    # We gaan elke rij van boven naar onder langs
    for rij_nummer in range(HEIGHT):
        # Bepaal hoe ver we zijn van boven naar onder
        # rij 0 = bovenaan, rij 899 = onderaan
        # positie is een getal tussen 0.0 (boven) en 1.0 (onder)
        positie = rij_nummer / HEIGHT
        
        # Bereken de groene kleur voor deze rij
        # Start bij 70 (donker groen), eindig bij 100 (licht groen)
        # 70 + (30 * positie) betekent:
        # - Als positie = 0.0 (boven): 70 + 0 = 70
        # - Als positie = 0.5 (midden): 70 + 15 = 85
        # - Als positie = 1.0 (onder): 70 + 30 = 100
        groen_waarde = 70 + int(30 * positie)
        
        # Teken een horizontale lijn over de hele breedte met deze kleur
        # (0, rij_nummer) = begin links op deze rij
        # (WIDTH, rij_nummer) = eindig rechts op deze rij (WIDTH = 600)
        pygame.draw.line(screen, (0, groen_waarde, 0), (0, rij_nummer), (WIDTH, rij_nummer))



def draw_glow_button(rect, text, base_color, glow_color, hover=False):
    """
    Parameters (ingrediënten):
    rect: pygame.Rect object - de positie en grootte van de knop (bijv. x=150, y=20, width=300, height=100)
    text: string - wat er op de knop moet staan (bijv. "DEAL HAND")
    base_color: tuple (R,G,B) - de achtergrondkleur van de knop (bijv. (0,100,0) = donkergroen)
    glow_color: tuple (R,G,B) - de kleur van de glow en rand (bijv. (255,215,0) = goud)
    hover: boolean (True/False) - of de muis over de knop zweeft
    """
    
    # 1. GLOW EFFECT - alleen als muis erover zweeft
    if hover:  # Als hover=True (dus als muis op knop staat)
        # Bereken hoe groot de glow moet zijn met een golfbeweging
        # glow_timer wordt elke frame met 1 verhoogd (in de main loop)
        # math.sin(glow_timer / 10) maakt een golf tussen -1 en 1
        # Voorbeeld: als glow_timer=0 → sin(0)=0 → 10 + 5*0 = 10
        #           als glow_timer=15 → sin(1.5)=0.997 → 10 + 5*0.997 ≈ 15
        #           als glow_timer=31 → sin(3.1)=-0.999 → 10 + 5*(-0.999) ≈ 5
        glow_size = 10 + int(5 * math.sin(glow_timer / 10))
        
        # Maak een grotere rechthoek dan de knop zelf voor de glow
        # inflate(glow_size, glow_size) betekent: maak zowel breedte als hoogte glow_size pixels groter
        # Als knop 300x100 is en glow_size=15 → glow wordt 315x115
        glow_rect = rect.inflate(glow_size, glow_size)
        
        # Maak een nieuw transparant "canvas" waarop we kunnen tekenen
        # pygame.SRCALPHA betekent: dit canvas heeft een alpha (transparantie) kanaal
        s = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        
        # Teken een glow op het transparante canvas
        # (*glow_color, 80): neem de glow_color (bijv. (255,215,0)) en voeg alpha 80 toe → (255,215,0,80)
        # 80/255 = ongeveer 31% transparantie (70% doorschijnend)
        # s.get_rect() geeft de volledige grootte van het canvas
        # border_radius=10 betekent: maak de hoeken rond met radius 10 pixels
        pygame.draw.rect(s, (*glow_color, 80), s.get_rect(), border_radius=10)
        
        # Plak het glow-canvas op het hoofdscherm
        # glow_rect.topleft is de positie waar de glow moet komen
        screen.blit(s, glow_rect.topleft)
    # EINDE van glow effect - dit was ALLEEN als hover=True
    
    # 2. DE KNOPSACHTERGROND
    # Teken een gevulde rechthoek met de basiskleur
    # rect = de positie/grootte die we als parameter kregen
    # 0 = vul de rechthoek volledig (geen lijnen, maar opvulling)
    # 10 = border radius: maak de hoeken rond (radius 10 pixels)
    pygame.draw.rect(screen, base_color, rect, 0, 10)
    
    # 3. DE RAND VAN DE KNOP
    # Teken de rand van de knop in de glow-kleur
    # 4 = dikte van de rand (4 pixels dik)
    pygame.draw.rect(screen, glow_color, rect, 4, 10)
    
    # 4. DE TEKST VAN DE KNOP
    # Maak de tekst surface (het "plaatje" van de tekst)
    # font.render maakt een afbeelding van de tekst
    text_surf = font.render(text, True, BLACK)  # Zwarte tekst
    
    # Maak een SCHADUW versie van de tekst (donkerder en transparant)
    # (0,0,0,128) = zwart met 50% transparantie (128/255 = 0.5)
    shadow_surf = font.render(text, True, (0, 0, 0, 128))
    
    # Bereken waar de tekst precies moet komen (in het midden van de knop)
    # get_rect(center=rect.center): maak een rechthoek rond de tekst en centreer die
    text_rect = text_surf.get_rect(center=rect.center)
    
    # Teken EERST de schaduw (2 pixels naar rechtsonder verschoven)
    screen.blit(shadow_surf, (text_rect.x + 2, text_rect.y + 2))
    
    # Teken DAN de echte tekst eroverheen
    screen.blit(text_surf, text_rect)
        


def draw_start_menu():
    """
    DEZE FUNCTIE MAAKT HET START MENU
    Het is zoals een restaurant menu: mooi, duidelijk, en nodigt uit om te kiezen.
    """

    # We gebruiken start_buttons in deze functie
    global start_buttons
    
    # 1. Maak de lijst voor buttons leeg (anders blijft oude buttons onthouden)
    start_buttons = []  # Net als een schoon whiteboard

    # 2. Teken dezelfde gradient achtergrond als in het spel
    #    Zodat menu en spel hetzelfde voelen
    draw_gradient_bg()

    # 3. ANIMATED TITLE - "BLACKJACK" dat op en neer beweegt
    # ------------------------------------------------------
    # Bereken Y positie: 150 pixels van boven + 10 pixels beweging
    # math.sin(glow_timer / 20) geeft een golf tussen -1 en 1
    # Dus: 150 + (10 * -1) = 140  OF  150 + (10 * 1) = 160
    title_y = 150 + int(10 * math.sin(glow_timer / 20))
    # Titel gaat van y=140 naar y=160 en terug (20 pixels verschil)

    # 4. TITEL GLOW EFFECT (5 lagen glow)
    # ------------------------------------
    # Dit maakt een zachte glow ROND de tekst
    # We tekenen 5 versies van de tekst, elk iets groter en transparanter
    for offset in range(5, 0, -1):  # offset = 5,4,3,2,1
        # Bereken transparantie: offset 5 → 45, 4 → 35, 3 → 25, etc.
        alpha = int(50 - offset * 10)  # 50-50=0? Nee: 50-5*10=0? Wacht...
        # Laat me corrigeren: 50 - (5*10) = 0, 50 - (4*10) = 10, etc.
        # Eigenlijk: alpha = 50 - (offset * 10)
        
        # Maak GLOW tekst (groter dan echte tekst)
        glow_surf = pygame.font.Font('freesansbold.ttf', 70 + offset * 2).render(
            "BLACKJACK", 
            True, 
            (255, 215, 0, alpha)  # Goud met transparantie
        )

        # Centreer de glow tekst
        glow_rect = glow_surf.get_rect(center=(WIDTH // 2, title_y))
        
        # Teken op scherm
        screen.blit(glow_surf, glow_rect)
    
    # 5. ECHTE TITEL (niet transparant, bovenop de glow)
    # ---------------------------------------------------
    title_surf = pygame.font.Font('freesansbold.ttf', 70).render(
        "BLACKJACK", 
        True, 
        GOLD  # Vol goud, geen transparantie
    )
    title_rect = title_surf.get_rect(center=(WIDTH // 2, title_y))
    screen.blit(title_surf, title_rect)

    # 6. SUBTITEL ("Test Your Luck!")
    # -------------------------------
    subtitle = smaller_font.render("Test Your Luck!", True, WHITE)
    # Centreer onder de titel: WIDTH//2 = midden, title_y + 80 = 80 pixels lager
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, title_y + 80))

    # 7. PLAY KNOB
    # ------------
    # Maak een rechthoek voor de knop: x=250, y=350, breedte=300, hoogte=100
    play_button = pygame.Rect(250, 350, 300, 100)

    # Vraag: waar is de muis?
    mouse_pos = pygame.mouse.get_pos()

    # Is muis OVER de knop?
    hover = play_button.collidepoint(mouse_pos)  # True of False

    # Teken de knop (gebruik onze bestaande glow_button functie!)
    draw_glow_button(play_button, "PLAY", GREEN_FELT, GOLD, hover)

    # Sla de knop op in start_buttons lijst voor later (klik detectie)
    start_buttons.append(play_button)

    # 8. STATISTIEKEN (Wins/Losses/Draws)
    # -----------------------------------
    stats_y = 500  # Start 500 pixels van boven

    # Maak een lijst met 3 tekstregels
    stats_texts = [
        f"Wins: {records[0]}",     # records[0] = wins
        f"Losses: {records[1]}",   # records[1] = losses
        f"Draws: {records[2]}"     # records[2] = draws
    ]

    # Loop door de 3 teksten en teken ze
    for i, text in enumerate(stats_texts):  # i = 0,1,2
        # Maak tekst surface
        stat_surf = tiny_font.render(text, True, GOLD)
        
        # Centreer elke regel
        x_pos = WIDTH // 2 - stat_surf.get_width() // 2
        y_pos = stats_y + i * 40  # Elke regel 40 pixels lager
        
        # Teken op scherm
        screen.blit(stat_surf, (x_pos, y_pos))

    # 9. DECORATIEVE CHIPS in de 4 hoeken
    # ------------------------------------
    # Posities: linksonder, rechtsonder, linksboven, rechtsboven
    chip_positions = [
        (80, 700),   # Linksonder
        (720, 700),  # Rechtsonder  
        (80, 250),   # Linksboven
        (720, 250)   # Rechtsboven
    ]

    # Voor elke chip positie
    for x, y in chip_positions:
        # Maak de chip een beetje bewegen (net als titel)
        offset = int(3 * math.sin(glow_timer / 15 + x))
        # +x zorgt dat elke chip andere timing heeft
        
        # Teken chip als 3 concentrische cirkels (3D effect)
        
        # Buitenste ring (donker goud, grootste)
        pygame.draw.circle(screen, DARK_GOLD, (x, y + offset), 25)
        
        # Midden ring (licht goud)
        pygame.draw.circle(screen, GOLD, (x, y + offset), 20)
        
        # Binnenste ring (donker goud, kleinste)
        pygame.draw.circle(screen, DARK_GOLD, (x, y + offset), 15)


class Particle:
    """
    Een Particle is één enkel deeltje/chip/sterretje.
    Denk aan: een muntstuk dat door de lucht vliegt.
    """
    
    def __init__(self, x, y, color, vx=None, vy=None):
        """
        Maakt een NIEUWE particle aan.
        Vergelijk het met: "Hier heb je een nieuw muntstuk"
        
        Parameters (wat je moet geven):
        - x, y: WAAR het muntstuk start (bijv. x=400, y=500 = midden scherm)
        - color: WELKE KLEUR het muntstuk heeft (GOLD, RED, WHITE)
        - vx, vy: HOE SNEL het beweegt (optioneel)
        """
        
        # Positie - WAAR het muntstuk nu is
        self.x = x  # Horizontale positie
        self.y = y  # Verticale positie
        
        # Kleur - HOE het muntstuk eruit ziet
        self.color = color  # Bijv. (255, 215, 0) = GOLD
        
        # Snelheid - HOE SNEL en WAARHEEN het gaat
        # vx = snelheid links/rechts (negatief = links, positief = rechts)
        # vy = snelheid omhoog/omlaag (negatief = omhoog, positief = omlaag)
        
        if vx is None:  # Als GEEN vx gegeven
            # Kies random snelheid tussen -3 en 3
            # Voorbeeld: -1.5 = beetje naar links, 2.8 = beetje naar rechts
            self.vx = random.uniform(-3, 3)
        else:
            self.vx = vx  # Gebruik de gegeven snelheid
            
        if vy is None:  # Als GEEN vy gegeven
            # Kies random snelheid tussen -8 en -3
            # ALTIJD NEGATIEF = altijd omhoog (want - getal)
            # Voorbeeld: -5.2 = redelijk snel omhoog
            self.vy = random.uniform(-8, -3)
        else:
            self.vy = vy  # Gebruik de gegeven snelheid
        
        # Levensduur - HOE LANG het muntstuk blijft
        self.life = 60  # 60 frames leven (bij 60fps = 1 seconde)
        # Elke frame gaat life -1, bij 0 is het muntstuk "dood"
        
        # Grootte - HOE GROOT het muntstuk is
        self.size = random.randint(3, 8)  # Tussen 3 en 8 pixels
        # Bijv. 5 = middelgroot, 8 = groot

    def update(self):
        """
        Update de particle: beweeg het en maak het ouder.
        Roept PyGame ELKE FRAME aan (60 keer per seconde).
        """
        # 1. BEWEEG het muntstuk
        self.x += self.vx  # Beweeg horizontaal
        self.y += self.vy  # Beweeg verticaal
        
        # 2. ZWAARTEKRACHT - trekt het muntstuk naar beneden
        # Elke frame: vy wordt 0.3 groter (positiever = meer omlaag)
        # Voorbeeld: vy = -5 (omhoog) → -4.7 → -4.4 → ... → 0 → 0.3 (omlaag)
        self.vy += 0.3
        
        # 3. WORD OUDER - verminder levensduur
        self.life -= 1  # Van 60 → 59 → 58 → ... → 0
        
        # 4. WORD KLEINER - naarmate het ouder wordt
        # max(1, ...) zorgt dat het NOOIT kleiner wordt dan 1 pixel
        self.size = max(1, self.size - 0.1)
        # Voorbeeld: size=8 → 7.9 → 7.8 → ... → 1.0
    
    def draw(self, screen):
        """
        Teken de particle op het scherm.
        """
        # 1. Bereken TRANSPARANTIE op basis van leeftijd
        # life=60 → alpha=255 (100% zichtbaar)
        # life=30 → alpha=127 (50% zichtbaar)
        # life=0 → alpha=0 (0% zichtbaar = onzichtbaar)
        alpha = int((self.life / 60) * 255)

        # 2. Maak een TRANSPARANT CANVAS om op te tekenen
        # Voorbeeld: size=5 → canvas wordt 10x10 pixels
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        
        # 3. Voeg transparantie toe aan de kleur
        # Voorbeeld: GOLD=(255,215,0) → met alpha=128 wordt het (255,215,0,128)
        color_with_alpha = (*self.color, alpha)

        # 4. Teken een CIRKEL op het canvas
        # Centreer de cirkel in het midden van het canvas
        pygame.draw.circle(s, color_with_alpha, (self.size, self.size), self.size)
        
        # 5. Plak het canvas op het hoofdscherm
        # Trek de helft van de grootte af om te centreren
        screen.blit(s, (int(self.x - self.size), int(self.y - self.size)))





    

    









# main game loop
run = True
load_card_assets(ASSETS_DIR, CARD_SIZE) # nieuw: laad alle kaarten

while run:
    # run game at our framerate an fill screen with bg color
    timer.tick(fps)
    # NIEUW: Update de glow timer voor de animatie - ZONDER DIT WERKT DE GLOW NIET!
    pulse_timer += 1
    glow_timer += 1
    if glow_timer > 1000:  # Voorkom dat het getal te groot wordt
        glow_timer = 0

    draw_gradient_bg()

    if menu_active:
        draw_start_menu()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                if start_buttons and start_buttons[0].collidepoint(event.pos):
                    pygame.mixer.Sound("Sounds/button-click-289742.mp3").play()
                    menu_active = False
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    reveal_dealer = False
                    add_score = True
    else:
        # initial deal to player and dealer
        if initial_deal:
            pygame.mixer.Sound("Sounds/mixkit-thin-metal-card-deck-shuffle-3175.wav").play()
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
                        pygame.mixer.Sound("Sounds/button-click-289742.mp3").play()
                        my_hand, game_deck = deal_cards(my_hand, game_deck, my_hand_images)
                        # 2. NIEUW: Maak 10 GOLDEN CHIPS vanuit de knop
                        for _ in range(10):  # _ betekent "ik tel niet mee, doe het gewoon 10x"
                            chip_particles.append(Particle(
                                buttons[0].centerx,  # x = midden van HIT knop
                                buttons[0].centery,  # y = midden van HIT knop
                                GOLD  # Kleur = GOLD
                            ))
                            # Elk muntstuk krijgt RANDOM snelheid (zie Particle.__init__)
                            # Dus ze vliegen alle kanten op!
                        
                    # allow player to end turn (stand)
                    elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                        pygame.mixer.Sound("Sounds/button-click-289742.mp3").play()
                        reveal_dealer = True
                        hand_active = False
                    elif len(buttons) == 3:
                        if buttons[2].collidepoint(event.pos):
                            pygame.mixer.Sound("Sounds/button-click-289742.mp3").play()
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
            if player_score > 21: # Alleen >21 is bust
                outcome = 1
            # Als precies 21, laat check_endgame() het afhandelen

        outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)

        
                

    pygame.display.flip()

pygame.quit()





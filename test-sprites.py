import pygame
import sys

# --- INIZIALIZZAZIONE ---
pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulator Pro: Pacco Animato")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 22, bold=True)

# --- COLORI E COSTANTI ---
WHITE = (255, 255, 255)
BLACK = (0, 10, 20)
BLUE_TEXT = (0, 102, 204)
MAX_CAPACITY = 20

# --- CARICAMENTO SPRITE ---
try:
    img_full = pygame.image.load("pacco.png").convert_alpha()
    img_full = pygame.transform.scale(img_full, (250, 250))
    img_ghost = img_full.copy()
    img_ghost.set_alpha(178)
    HAS_IMAGE = True
except:
    HAS_IMAGE = False
    print("ERRORE: pacco.png non trovato!")

# --- VARIABILI DI STATO ---
stage = "INPUT"
input_text = ""
item_count = 0
max_items = 0
current_weight = 0
total_packages = 0
box_x, box_y = 175, 200
is_shipping = False
target_weight = 0


def draw_ui():
    pygame.draw.rect(screen, (230, 230, 230), (0, 0, WIDTH, 100))
    txt_items = font.render(f"Oggetti: {item_count} / {max_items}", True, BLACK)
    txt_sent = font.render(f"Pacchi Spediti: {total_packages}", True, (200, 0, 0))
    screen.blit(txt_items, (20, 20))
    screen.blit(txt_sent, (20, 50))


# --- LOOP PRINCIPALE ---
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if stage == "INPUT":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_text:
                    max_items = int(input_text)
                    stage = "SIMULATION"
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isdigit():
                    input_text += event.unicode

        elif stage == "SIMULATION" and not is_shipping:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    stage = "RESULTS"
                elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                    val = int(event.unicode)
                    item_count += 1
                    if current_weight + val > MAX_CAPACITY:
                        total_packages += 1
                        target_weight = val
                        is_shipping = True
                    else:
                        current_weight += val
                        if item_count >= max_items:
                            total_packages += 1
                            stage = "RESULTS"

    # --- LOGICA ANIMAZIONE ---
    if is_shipping:
        box_x += 20
        if box_x > WIDTH:
            box_x = -250
            current_weight = target_weight
            is_shipping = False  # Importante: ferma l'animazione d'uscita
            if item_count >= max_items: stage = "RESULTS"
    elif stage == "SIMULATION" and box_x < 175:
        box_x += 20
        if box_x > 175: box_x = 175

    # --- RENDERING (QUESTA PARTE MANCAVA O ERA ROTTA) ---
    if stage == "INPUT":
        prompt = font.render("Quanti oggetti totali?", True, BLACK)
        val_txt = font.render(f"> {input_text}", True, BLUE_TEXT)
        screen.blit(prompt, (WIDTH // 2 - 100, 250))
        screen.blit(val_txt, (WIDTH // 2 - 20, 300))

    elif stage == "SIMULATION":
        draw_ui()
        if HAS_IMAGE:
            screen.blit(img_ghost, (box_x, box_y))
            fill_h = int((current_weight / MAX_CAPACITY) * 250)
            if fill_h > 0:
                crop_area = pygame.Rect(0, 250 - fill_h, 250, fill_h)
                screen.blit(img_full, (box_x, box_y + 250 - fill_h), crop_area)
        else:
            pygame.draw.rect(screen, (139, 69, 19), (box_x, box_y, 250, 250), 2)

        p_txt = font.render(f"{current_weight} / {MAX_CAPACITY} kg", True, BLACK)
        screen.blit(p_txt, (box_x + 70, box_y - 30))

    elif stage == "RESULTS":
        res_txt = font.render(f"FINE! Pacchi: {total_packages}. Esci col tasto X", True, (0, 150, 0))
        screen.blit(res_txt, (150, 250))

    # --- IL COMANDO MAGICO PER NON VEDERE NERO ---
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
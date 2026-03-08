import pygame
import sys
import time

# --- Inizializzazione ---
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Package Simulator Pro - Animated")
font = pygame.font.SysFont("Arial", 22)
big_font = pygame.font.SysFont("Arial", 32, bold=True)
clock = pygame.time.Clock()

# --- Colori ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 150, 0)
LIGHT_GRAY = (220, 220, 220)
# Colori per la scatola di cartone
BROWN_DARK = (139, 69, 19)  # Marrone scuro per i bordi
BROWN_LIGHT = (210, 180, 140)  # Marrone chiaro per l'interno (Tan)
PACKAGE_FILL = (100, 200, 255)  # Azzurro per il contenuto

# --- Variabili di Stato ---
stage = "INPUT_MAX"  # INPUT_MAX, SIMULATION, RESULTS
input_text = ""
max_items = 0
item_count = 0
current_weight = 0
packages_sent = 0
total_weight_sent = 0
message = ""

# --- Variabili per l'Animazione ---
# Posizione standard della scatola
BOX_START_X = (SCREEN_WIDTH // 2) - 100  # Centrato
BOX_START_Y = 200
box_x = BOX_START_X
box_y = BOX_START_Y
BOX_WIDTH = 200
BOX_HEIGHT = 300
is_animating = False
animation_type = ""  # "SHIPPING" o "ARRIVING"


# --- Funzione per disegnare una scatola "stilizzata" ---
def draw_styled_box(surface, x, y, width, height, weight):
    # 1. Fondo della scatola (marrone chiaro)
    pygame.draw.rect(surface, BROWN_LIGHT, (x, y, width, height))

    # 2. Contenuto (azzurro, proporzionale al peso)
    fill_h = (weight / 20) * height
    # Disegniamo il contenuto sopra il fondo, partendo dal basso
    if weight > 0:
        pygame.draw.rect(surface, PACKAGE_FILL, (x, y + height - fill_h, width, fill_h))

    # 3. Bordi della scatola (marrone scuro, spessi)
    pygame.draw.rect(surface, BROWN_DARK, (x, y, width, height), 5)

    # 4. Dettagli stilizzati (linee per nastro adesivo o pieghe)
    # Linea orizzontale superiore (nastro)
    pygame.draw.line(surface, BROWN_DARK, (x, y + 20), (x + width, y + 20), 2)
    # Linea orizzontale inferiore (nastro)
    pygame.draw.line(surface, BROWN_DARK, (x, y + height - 20), (x + width, y + height - 20), 2)
    # Linea verticale centrale (piega)
    pygame.draw.line(surface, BROWN_DARK, (x + width // 2, y + 20), (x + width // 2, y + height - 20), 1)

    # 5. Etichetta del peso (testo sul pacco)
    weight_text = font.render(f"{weight} kg", True, BLACK)
    surface.blit(weight_text,
                 (x + width // 2 - weight_text.get_width() // 2, y + height // 2 - weight_text.get_height() // 2))


# --- Loop Principale ---
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- LOGICA: INSERIMENTO MASSIMO ITEM ---
        if stage == "INPUT_MAX":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_text != "":
                    max_items = int(input_text)
                    stage = "SIMULATION"
                    # Reset variabili simulazione
                    item_count = 0
                    current_weight = 0
                    packages_sent = 0
                    total_weight_sent = 0
                    box_x = BOX_START_X  # Assicuriamoci che la scatola sia in posizione
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isdigit():
                    input_text += event.unicode

        # --- LOGICA: SIMULAZIONE (No input se in animazione) ---
        elif stage == "SIMULATION" and not is_animating:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    stage = "RESULTS"
                elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                    weight = int(event.unicode)

                    if current_weight + weight > 20:
                        # IL PACCO È PIENO: Avvia animazione di spedizione
                        print(f"Pacco pieno ({current_weight}kg)! Avvio spedizione...")
                        packages_sent += 1
                        total_weight_sent += current_weight

                        # Salviamo il peso per il nuovo pacco
                        next_weight = weight
                        item_count += 1  # Contiamo l'item che ha fatto traboccare il pacco

                        # Attiva l'animazione d'uscita
                        is_animating = True
                        animation_type = "SHIPPING"
                        current_weight = 0  # Svuotiamo visivamente mentre esce

                        # Nota: Non aggiorniamo 'current_weight' con 'next_weight' qui.
                        # Lo faremo alla fine dell'animazione d'uscita.

                    else:
                        current_weight += weight
                        item_count += 1

                    # Controllo fine item (solo se non stiamo già animando una spedizione)
                    if not is_animating and item_count >= max_items:
                        # Gestiamo l'ultimo pacco e andiamo ai risultati
                        packages_sent += 1
                        total_weight_sent += current_weight
                        stage = "RESULTS"

    # --- AGGIORNAMENTO ANIMAZIONI ---
    if is_animating:
        if animation_type == "SHIPPING":
            # Il pacco esce a destra
            box_x += 15  # Velocità di uscita
            if box_x > SCREEN_WIDTH:
                # È uscito completamente!
                animation_type = "ARRIVING"
                box_x = -BOX_WIDTH  # Riposiziona a sinistra, fuori schermo
                # Ora che il vecchio è uscito, iniziamo il nuovo con il peso avanzato
                current_weight = next_weight

                # Controllo immediato se anche il nuovo peso completa gli item
                if item_count >= max_items:
                    # Abbiamo finito gli item proprio ora!
                    # Spediamo anche questo e andiamo ai risultati
                    packages_sent += 1
                    total_weight_sent += current_weight
                    stage = "RESULTS"
                    is_animating = False  # Fine animazione, vai ai risultati

        elif animation_type == "ARRIVING":
            # Il nuovo pacco entra da sinistra
            box_x += 15
            if box_x >= BOX_START_X:
                # È arrivato in posizione!
                box_x = BOX_START_X
                is_animating = False  # Fine animazione totale

    # --- DISEGNO (RENDERING) ---
    if stage == "INPUT_MAX":
        # Sfondo grigio chiaro per l'input
        pygame.draw.rect(screen, LIGHT_GRAY, (50, 150, SCREEN_WIDTH - 100, 200), 0, 15)
        msg = big_font.render("Quanti item vuoi spedire?", True, BLACK)
        screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, 200))
        val_surface = font.render(f"Inserisci e premi INVIO: {input_text}", True, BROWN_DARK)
        screen.blit(val_surface, (SCREEN_WIDTH // 2 - val_surface.get_width() // 2, 260))

    elif stage == "SIMULATION":
        # Area Info (Sfondo fisso in alto)
        pygame.draw.rect(screen, LIGHT_GRAY, (0, 0, SCREEN_WIDTH, 130))
        screen.blit(font.render(f"Item processati: {item_count} / {max_items}", True, BLACK), (30, 20))
        screen.blit(font.render(f"Pacchi spediti: {packages_sent}", True, RED), (30, 50))
        screen.blit(font.render(f"Peso totale inviato: {total_weight_sent} kg", True, GREEN), (30, 80))

        # Barra di stato/istruzioni in basso
        pygame.draw.rect(screen, BLACK, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        instr = font.render("Premi 1-9 per aggiungere peso, 0 per STOP", True, WHITE)
        screen.blit(instr, (SCREEN_WIDTH // 2 - instr.get_width() // 2, SCREEN_HEIGHT - 35))

        # DISEGNO LA SCATOLA ANIMATA
        # Usiamo le variabili box_x e box_y che cambiano durante l'animazione
        draw_styled_box(screen, box_x, box_y, BOX_WIDTH, BOX_HEIGHT, current_weight)

    elif stage == "RESULTS":
        pygame.draw.rect(screen, LIGHT_GRAY, (50, 100, SCREEN_WIDTH - 100, 400), 0, 15)
        res_title = big_font.render("REPORT SPEDIZIONE", True, GREEN)
        screen.blit(res_title, (SCREEN_WIDTH // 2 - res_title.get_width() // 2, 130))

        results = [
            f"Pacchi totali inviati: {packages_sent}",
            f"Peso totale inviato: {total_weight_sent} kg",
            f"Media peso per pacco: {total_weight_sent / packages_sent:.1f} kg" if packages_sent > 0 else "N/A",
            "",
            "Simulazione completata.",
            "Chiudi la finestra per uscire."
        ]

        y_offset = 200
        for line in results:
            color = BLACK if "Chiudi" not in line else RED
            res_text = font.render(line, True, color)
            screen.blit(res_text, (100, y_offset))
            y_offset += 30

    pygame.display.flip()
    clock.tick(60)  # 60 FPS per animazioni fluide

pygame.quit()
sys.exit()
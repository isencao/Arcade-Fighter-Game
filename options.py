import pygame
import sys
import subprocess

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Background Selection")
pygame.display.set_icon(pygame.image.load("assets/images/icons/my_icon.png"))

# Renkler ve fontlar
BG_COLOR = (30, 30, 40)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
LIGHT_BLUE = (100, 149, 237)
DARK_GRAY = (60, 60, 60)
RED = (200, 50, 50)
BLACK = (0, 0, 0)

font = pygame.font.Font("assets/fonts/nexa.ttf", 30)
small_font = pygame.font.Font("assets/fonts/nexa.ttf", 20)

# Harita seçenekleri
map_options = [
    {"name": "Terra Arida", "file": "background1.png"},
    {"name": "Silva Obscura", "file": "background2.png"},
    {"name": "Castellum Rubrum", "file": "background3.png"},
    {"name": "Glacies Vallis", "file": "background4.png"},
    {"name": "Ignis Fossa", "file": "background5.png"}
]

buttons = []
for i, option in enumerate(map_options):
    image = pygame.image.load(f"assets/images/background/{option['file']}")
    image = pygame.transform.scale(image, (180, 100))
    rect = image.get_rect(topleft=(50 + i * 190, 100))
    buttons.append((image, rect, option))

# Butonlar
start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 400, 200, 60)
back_button = pygame.Rect(30, SCREEN_HEIGHT - 70, 120, 40)
settings_button = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 70, 120, 40)
howto_button = pygame.Rect(SCREEN_WIDTH - 180, SCREEN_HEIGHT - 130, 160, 40)
choose_char_button = pygame.Rect(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 190, 180, 40)
button_width = 180
button_height = 40
button_gap = 40  # iki buton arası boşluk
total_width = 2 * button_width + button_gap
start_x = (SCREEN_WIDTH - total_width) // 2
y_pos = 320

singleplayer_button = pygame.Rect(start_x, y_pos, button_width, button_height)
multiplayer_button = pygame.Rect(start_x + button_width + button_gap, y_pos, button_width, button_height)


settings_open = False
volume = 5
round_time = 60
selected_bg = None
game_mode = "multiplayer"
running = True

settings_panel = pygame.Rect(SCREEN_WIDTH - 320, SCREEN_HEIGHT - 400, 300, 250)
plus_rect = pygame.Rect(settings_panel.right - 50, settings_panel.top + 50, 30, 30)
minus_rect = pygame.Rect(settings_panel.left + 20, settings_panel.top + 50, 30, 30)
roundtime_button = pygame.Rect(settings_panel.centerx - 60, settings_panel.top + 150, 120, 30)

def save_volume(vol):
    with open("volume.txt", "w") as f:
        f.write(str(vol / 10))

def save_round_time(seconds):
    with open("round_time.txt", "w") as f:
        f.write(str(seconds))

def save_background(bg_name):
    with open("selected_background.txt", "w") as file:
        file.write(bg_name)

def draw_text(text, font, color, surface, x, y, center=False):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

clock = pygame.time.Clock()

while running:
    screen.fill(BG_COLOR)
    draw_text("MAPS", font, WHITE, screen, SCREEN_WIDTH // 2, 40, center=True)

    for image, rect, option in buttons:
        screen.blit(image, rect)
        draw_text(option["name"], small_font, WHITE, screen, rect.centerx, rect.bottom + 20, center=True)

        if rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, LIGHT_BLUE, rect, 3)

        if selected_bg == option["file"]:
            pygame.draw.rect(screen, RED, rect, 4)

    # Mod seçim butonları
    pygame.draw.rect(screen, LIGHT_BLUE if game_mode == "singleplayer" else DARK_GRAY, singleplayer_button, border_radius=10)
    draw_text("SINGLEPLAYER", small_font, WHITE, screen, singleplayer_button.centerx, singleplayer_button.centery, center=True)

    pygame.draw.rect(screen, LIGHT_BLUE if game_mode == "multiplayer" else DARK_GRAY, multiplayer_button, border_radius=10)
    draw_text("MULTIPLAYER", small_font, WHITE, screen, multiplayer_button.centerx, multiplayer_button.centery, center=True)

    # Butonları çiz
    pygame.draw.rect(screen, GRAY, start_button, border_radius=10)
    draw_text("PLAY", font, WHITE, screen, start_button.centerx, start_button.centery, center=True)

    pygame.draw.rect(screen, RED, back_button, border_radius=10)
    draw_text("BACK", small_font, WHITE, screen, back_button.centerx, back_button.centery, center=True)

    pygame.draw.rect(screen, DARK_GRAY, settings_button, border_radius=10)
    draw_text("SETTINGS", small_font, WHITE, screen, settings_button.centerx, settings_button.centery, center=True)

    pygame.draw.rect(screen, DARK_GRAY, howto_button, border_radius=10)
    draw_text("HOW TO PLAY", small_font, WHITE, screen, howto_button.centerx, howto_button.centery, center=True)

    pygame.draw.rect(screen, DARK_GRAY, choose_char_button, border_radius=10)
    draw_text("CHOOSE CHARACTERS", small_font, WHITE, screen, choose_char_button.centerx, choose_char_button.centery, center=True)

    # Ayarlar paneli
    if settings_open:
        pygame.draw.rect(screen, (20, 20, 20), settings_panel, border_radius=10)
        draw_text("Sound", small_font, WHITE, screen, settings_panel.centerx, settings_panel.top + 30, center=True)
        draw_text(str(volume), small_font, WHITE, screen, settings_panel.centerx, settings_panel.top + 65, center=True)
        pygame.draw.rect(screen, LIGHT_BLUE, plus_rect)
        draw_text("+", small_font, BLACK, screen, plus_rect.centerx, plus_rect.centery, center=True)
        pygame.draw.rect(screen, LIGHT_BLUE, minus_rect)
        draw_text("-", small_font, BLACK, screen, minus_rect.centerx, minus_rect.centery, center=True)

        draw_text("Time: " + str(round_time) + "s", small_font, WHITE, screen, settings_panel.centerx, settings_panel.top + 120, center=True)
        pygame.draw.rect(screen, LIGHT_BLUE, roundtime_button)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if singleplayer_button.collidepoint(mx, my):
                game_mode = "singleplayer"
            elif multiplayer_button.collidepoint(mx, my):
                game_mode = "multiplayer"

            if start_button.collidepoint(mx, my) and selected_bg:
                save_background(selected_bg)
                save_round_time(round_time)
                with open("mode.txt", "w") as f:
                    f.write(game_mode)
                subprocess.Popen(["python", "main.py"])
                running = False

            if back_button.collidepoint(mx, my):
                subprocess.Popen(["python", "menu.py"])
                running = False

            if settings_button.collidepoint(mx, my):
                settings_open = not settings_open

            if howto_button.collidepoint(mx, my):
                subprocess.Popen(["python", "how_to_play.py"])

            if choose_char_button.collidepoint(mx, my):
                subprocess.Popen(["python", "character_select.py"])

            if settings_open:
                if plus_rect.collidepoint(mx, my) and volume < 10:
                    volume += 1
                    save_volume(volume)
                elif minus_rect.collidepoint(mx, my) and volume > 0:
                    volume -= 1
                    save_volume(volume)
                elif roundtime_button.collidepoint(mx, my):
                    round_time = 30 if round_time == 90 else round_time + 30
            else:
                for image, rect, option in buttons:
                    if rect.collidepoint(mx, my):
                        selected_bg = option["file"]

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()

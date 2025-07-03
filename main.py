import pygame
from pygame import mixer
import os
import subprocess
import json
from fighter import Fighter

pygame.init()
mixer.init()

# --- Oyun modu oku ---
mode = "multiplayer"
if os.path.exists("mode.txt"):
    try:
        with open("mode.txt", "r") as f:
            mode = f.read().strip()
    except:
        mode = "multiplayer"

volume_level = 0.5
if os.path.exists("volume.txt"):
    try:
        with open("volume.txt", "r") as f:
            volume_level = float(f.read().strip())
    except:
        volume_level = 0.5

ROUND_TIME = 60
if os.path.exists("round_time.txt"):
    try:
        with open("round_time.txt", "r") as f:
            ROUND_TIME = int(f.read().strip())
    except:
        ROUND_TIME = 60

default_p1 = "assets/images/split_medieval_warrior_3"
default_p2 = "assets/images/split_martial_hero_2"

martialhero3_folder = "assets/images/martialhero3"
martialhero3_animation_steps = [10, 8, 3, 7, 6, 9, 3, 11, 3]
martialhero3_data = (160, 2.5, [70, 68])

heroknight_folder = "assets/images/heroknight"
heroknight_animation_steps = [11, 8, 3, 7, 7, 1, 4, 11, 3]
heroknight_data = (160, 2.5, [72, 86])

if os.path.exists("selected_chars.json"):
    try:
        with open("selected_chars.json", "r") as f:
            char_data = json.load(f)
            p1_sprite_folder = char_data.get("player1", default_p1)
            p2_sprite_folder = char_data.get("player2", default_p2)
    except:
        p1_sprite_folder = default_p1
        p2_sprite_folder = default_p2
else:
    p1_sprite_folder = default_p1
    p2_sprite_folder = default_p2

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arcade Fighter")
pygame.display.set_icon(pygame.image.load("assets/images/icons/my_icon.png"))

clock = pygame.time.Clock()
FPS = 60

count_font = pygame.font.Font("assets/fonts/ARCADE.ttf", 80)
score_font = pygame.font.Font("assets/fonts/ARCADE.ttf", 35)
small_font = pygame.font.Font("assets/fonts/ARCADE.ttf", 20)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (50, 50, 50)
TURQUOISE = (0, 180, 200)
ORANGE = (255, 140, 0)

def load_selected_background():
    try:
        with open("selected_background.txt", "r") as file:
            filename = file.read().strip()
            return os.path.join("assets", "images", "background", filename)
    except FileNotFoundError:
        return "assets/images/background/background2.png"

bg_image = pygame.image.load(load_selected_background()).convert_alpha()

def draw_bg():
    scaled = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled, (0, 0))

def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, DARK_GREY, (x, y, 400, 30))
    pygame.draw.rect(screen, TURQUOISE, (x, y, 400 * ratio, 30))

def draw_text(text, font, color, x, y, align_center=False):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if align_center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(img, rect)

back_button = pygame.Rect(20, SCREEN_HEIGHT - 60, 100, 40)

pygame.mixer.music.set_volume(volume_level)
pygame.mixer.music.load("assets/audio/fighter.mp3")
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(volume_level)
magic_fx = pygame.mixer.Sound("assets/audio/sword1.mp3")
magic_fx.set_volume(volume_level)

FIGHTER_DATA = [80, 6, [30, 20]]
P1_ANIMATION_STEPS = [10, 6, 2, 2, 4, 4, 5, 3, 9]
P2_ANIMATION_STEPS = [4, 8, 2, 2, 4, 4, 3, 7]

intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]
MAX_SCORE = 3
game_over = False
winner_text = ""
round_over = False
ROUND_OVER_COOLDOWN = 2000
start_ticks = pygame.time.get_ticks()

fighter_1 = Fighter(1, 200, 310, False, FIGHTER_DATA, p1_sprite_folder, P1_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 700, 310, True, FIGHTER_DATA, p2_sprite_folder, P2_ANIMATION_STEPS, magic_fx)
fighter_3 = Fighter(3, 400, 310, False, martialhero3_data, martialhero3_folder, martialhero3_animation_steps, None)
fighter_4 = Fighter(4, 360, 340, False, heroknight_data, heroknight_folder, heroknight_animation_steps, None)

run = True
while run:
    clock.tick(FPS)
    draw_bg()
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("P1", score_font, WHITE, 20, 60)
    draw_text("P2", score_font, WHITE, 580, 60)

    elapsed = (pygame.time.get_ticks() - start_ticks) // 1000
    time_left = max(0, ROUND_TIME - elapsed)
    draw_text(f"Time: {time_left}s", small_font, WHITE, SCREEN_WIDTH // 2, 20, align_center=True)

    pygame.draw.rect(screen, (60, 60, 60), back_button, border_radius=10)
    draw_text("BACK", small_font, WHITE, back_button.centerx, back_button.centery, align_center=True)

    if intro_count <= 0 and not round_over and time_left > 0 and not game_over:
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)

        if mode == "singleplayer":
            if fighter_2.alive:
                distance = fighter_1.rect.centerx - fighter_2.rect.centerx
                if abs(distance) > 60:
                    fighter_2.vel_x = 3 if distance > 0 else -3
                    fighter_2.rect.x += fighter_2.vel_x
                    fighter_2.running = True
                else:
                    fighter_2.vel_x = 0
                    fighter_2.running = False
                    if not fighter_2.attacking:
                        fighter_2.attack(fighter_1)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
        else:
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)

    elif time_left == 0 and not round_over and not game_over:
        round_over = True
        round_over_time = pygame.time.get_ticks()
        if fighter_1.health > fighter_2.health:
            score[0] += 1
        elif fighter_2.health > fighter_1.health:
            score[1] += 1

    elif intro_count > 0:
        draw_text(str(intro_count), count_font, ORANGE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3, align_center=True)
        if pygame.time.get_ticks() - last_count_update >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    fighter_1.update()
    fighter_2.update()
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    if not round_over and not game_over:
        if not fighter_1.alive:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif not fighter_2.alive:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()

        if score[0] == MAX_SCORE:
            game_over = True
            winner_text = "PLAYER 1 WINS"
        elif score[1] == MAX_SCORE:
            game_over = True
            winner_text = "PLAYER 2 WINS"

    else:
        draw_text("TIME OUT" if time_left == 0 else "VICTORY", count_font, ORANGE, SCREEN_WIDTH // 2, 100, align_center=True)
        score_display = f"{score[0]} - {score[1]}"
        score_surface = score_font.render(f"Score: {score_display}", True, WHITE)
        screen.blit(score_surface, (SCREEN_WIDTH // 2 - score_surface.get_width() // 2, 240))

        if game_over:
            draw_text(winner_text, count_font, ORANGE, SCREEN_WIDTH // 2, 300, align_center=True)
            draw_text("Press R to Restart", small_font, WHITE, SCREEN_WIDTH // 2, 360, align_center=True)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                score = [0, 0]
                game_over = False
                round_over = False
                intro_count = 3
                start_ticks = pygame.time.get_ticks()
                fighter_1 = Fighter(1, 200, 310, False, FIGHTER_DATA, p1_sprite_folder, P1_ANIMATION_STEPS, sword_fx)
                fighter_2 = Fighter(2, 700, 310, True, FIGHTER_DATA, p2_sprite_folder, P2_ANIMATION_STEPS, magic_fx)

        elif pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            start_ticks = pygame.time.get_ticks()
            fighter_1 = Fighter(1, 200, 310, False, FIGHTER_DATA, p1_sprite_folder, P1_ANIMATION_STEPS, sword_fx)
            fighter_2 = Fighter(2, 700, 310, True, FIGHTER_DATA, p2_sprite_folder, P2_ANIMATION_STEPS, magic_fx)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_button.collidepoint(pygame.mouse.get_pos()):
                subprocess.Popen(["python", "options.py"])
                run = False

    pygame.display.update()

pygame.quit()

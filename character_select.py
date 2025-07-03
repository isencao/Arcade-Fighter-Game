import pygame
import sys
import json
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Choose Characters")
pygame.display.set_icon(pygame.image.load("assets/images/icons/my_icon.png"))

font = pygame.font.Font("assets/fonts/nexa.ttf", 24)
title_font = pygame.font.Font("assets/fonts/nexa.ttf", 40)
small_font = pygame.font.Font("assets/fonts/nexa.ttf", 20)

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BG = (20, 20, 30)

characters = [
    {"name": "Medieval Warrior", "folder": "assets/images/split_medieval_warrior_3"},
    {"name": "Martial Hero", "folder": "assets/images/split_martial_hero_2"},
    {"name": "Ninja", "folder": "assets/images/split_ninja"},
    {"name": "Martial Hero 3", "folder": "assets/images/martialhero3"},
    {"name": "Hero Knight", "folder": "assets/images/heroknight"}


]

player1 = 0
player2 = 1
selecting_player = 1  # Önce P1, sonra P2

clock = pygame.time.Clock()
running = True

def draw_text(text, font, color, x, y, center=False):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(img, rect)

while running:
    screen.fill(BG)

    draw_text("CHOOSE CHARACTERS", title_font, WHITE, SCREEN_WIDTH // 2, 40, center=True)

    draw_text("Player 1", font, WHITE, 200, 120, center=True)
    draw_text("Player 2", font, WHITE, 600, 120, center=True)

    for i, char in enumerate(characters):
        color1 = GREEN if i == player1 else WHITE
        color2 = GREEN if i == player2 else WHITE

        draw_text(char["name"], font, color1, 200, 170 + i * 40, center=True)
        draw_text(char["name"], font, color2, 600, 170 + i * 40, center=True)

    if selecting_player == 1:
        draw_text("Select Player 1 - ENTER to Confirm", small_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60, center=True)
        draw_text("↑ / ↓ to choose", small_font, YELLOW, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30, center=True)
        draw_text("", font, YELLOW, 130, 170 + player1 * 40, center=True)
    elif selecting_player == 2:
        draw_text("Select Player 2 - ENTER to Confirm", small_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60, center=True)
        draw_text("↑ / ↓ to choose", small_font, YELLOW, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30, center=True)
        draw_text("", font, YELLOW, 530, 170 + player2 * 40, center=True)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            elif event.key == pygame.K_UP:
                if selecting_player == 1:
                    player1 = (player1 - 1) % len(characters)
                elif selecting_player == 2:
                    player2 = (player2 - 1) % len(characters)

            elif event.key == pygame.K_DOWN:
                if selecting_player == 1:
                    player1 = (player1 + 1) % len(characters)
                elif selecting_player == 2:
                    player2 = (player2 + 1) % len(characters)

            elif event.key == pygame.K_RETURN:
                if selecting_player == 1:
                    selecting_player = 2
                else:
                    selected = {
                        "player1": characters[player1]["folder"],
                        "player2": characters[player2]["folder"]
                    }
                    with open("selected_chars.json", "w") as f:
                        json.dump(selected, f)
                    running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

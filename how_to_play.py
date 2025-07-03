
import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("How to Play")
pygame.display.set_icon(pygame.image.load("assets/images/icons/my_icon.png"))

font = pygame.font.Font("assets/fonts/nexa.ttf", 24)
title_font = pygame.font.Font("assets/fonts/nexa.ttf", 40)
WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
BG = (25, 25, 40)

lines = [
    "P1: W A S D → Movement",
    "P1: R → Attack 1, T → Attack 2",
    "P2: Arrow Keys → Movement",
    "P2: NumPad 1 → Attack 1, NumPad 2 → Attack 2",
    "",
    "SPACE = Exit this screen.",
]

running = True
while running:
    screen.fill(BG)

    title = title_font.render("HOW TO PLAY", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 40))

    for i, line in enumerate(lines):
        txt = font.render(line, True, WHITE)
        screen.blit(txt, (60, 120 + i * 40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()

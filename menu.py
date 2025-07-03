import pygame
import sys
import subprocess

pygame.init()


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600


BG_COLOR = (35, 33, 35)  

WHITE = (253, 18, 43)  


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arcade Fighter - Menü")
icon = pygame.image.load("assets/images/icons/my_icon.png")  
pygame.display.set_icon(icon)

bg_image = pygame.image.load("assets/images/icons/menu.png").convert_alpha()





# Fontlar ve buton ayarları
font = pygame.font.Font("assets/fonts/ARCADE.ttf", 50)
button_width = 220  
button_height = 70
button_x = (SCREEN_WIDTH - button_width) // 2
button_y = 400


clock = pygame.time.Clock()
FPS = 60


logo_final_y = 100
logo_speed = 15

running = True
while running:
    screen.fill((0, 0, 0))  

    
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))  

    

  
    pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height), border_radius=10)
    start_text = font.render("START", True, BG_COLOR)
    screen.blit(start_text, (button_x + (button_width - start_text.get_width()) // 2, button_y + 10))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                subprocess.run(["python", "options.py"])  
                running = False

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()

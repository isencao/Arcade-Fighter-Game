import pygame
import os

class Fighter():
    def __init__(self, player, x, y, flip, data, image_folder, animation_steps, sound):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(image_folder, animation_steps)
        self.action = 0
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.health = 100
        self.alive = True

    def load_images(self, folder_path, animation_steps):
        animation_list = []
        for i, num_frames in enumerate(animation_steps):
            temp_img_list = []
            for frame_num in range(num_frames):
                img_path = os.path.join(folder_path, str(i), f"{frame_num}.png")
                if os.path.exists(img_path):
                    img = pygame.image.load(img_path).convert_alpha()
                    img = pygame.transform.scale(img, (self.size * self.image_scale, self.size * self.image_scale))
                    temp_img_list.append(img)
                else:
                    print(f"[Uyarı] Eksik dosya: {img_path}")
            if not temp_img_list:
                print(f"[Uyarı] {folder_path}/{i}/ dizini tamamen boş.")
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        key = pygame.key.get_pressed()

        if not self.attacking and self.alive and not round_over:
            if self.player == 1:
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                if key[pygame.K_w] and not self.jump:
                    self.vel_y = -30
                    self.jump = True
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(target)
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2

            if self.player == 2:
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                if key[pygame.K_UP] and not self.jump:
                    self.vel_y = -30
                    self.jump = True
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(target)
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
                        self.attack_type = 2

        self.vel_y += GRAVITY
        dy += self.vel_y

        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        hit_index = len(self.animation_list) - 2
        death_index = len(self.animation_list) - 1

        if self.health <= 0:
            self.health = 0
            if self.alive:
                self.alive = False
                self.update_action(death_index)
        elif self.hit:
            self.update_action(hit_index)
        elif self.attacking:
            if self.attack_type == 1:
                self.update_action(4)
            elif self.attack_type == 2:
                self.update_action(5)
        elif self.jump:
            self.update_action(2)
        elif self.running:
            self.update_action(1)
        else:
            self.update_action(0)

        animation_cooldown = 50
        if len(self.animation_list[self.action]) > 0:
            self.image = self.animation_list[self.action][self.frame_index]

            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()

            if self.frame_index >= len(self.animation_list[self.action]):
                if not self.alive:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.frame_index = 0
                    if self.action in [4, 5]:
                        self.attacking = False
                        self.attack_cooldown = 20
                    if self.action == hit_index:
                        self.hit = False
                        self.attacking = False
                        self.attack_cooldown = 20

    def attack(self, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.attack_type = 1  # Botlar için animasyonu tetiklemek adına varsayılan saldırı tipi
            if self.attack_sound:
                self.attack_sound.play()
            attacking_rect = pygame.Rect(
                self.rect.centerx - (2 * self.rect.width * self.flip),
                self.rect.y,
                2 * self.rect.width,
                self.rect.height
            )
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True
                target.attacking = False

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        if len(self.animation_list[self.action]) > 0:
            img = pygame.transform.flip(self.image, self.flip, False)
            surface.blit(img, (
                self.rect.x - (self.offset[0] * self.image_scale),
                self.rect.y - (self.offset[1] * self.image_scale)
            ))

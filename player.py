import pygame

# Player class
class Player:
    def __init__(self, jump_strength=-10, gravity=0.5):
        self.rect = pygame.Rect(100, 500, 50, 50)
        self.vel_y = 0
        self.attack_cooldown = 0
        self.attack_rect = pygame.Rect(0, 0, 0, 0)
        self.jump_strength = jump_strength
        self.gravity = gravity

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False

        # Apply gravity
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # Attack
        if keys[pygame.K_z] and self.attack_cooldown == 0:
            self.attack()

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def attack(self):
        self.attack_rect = pygame.Rect(self.rect.right, self.rect.top, 20, self.rect.height)
        self.attack_cooldown = 30
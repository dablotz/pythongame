import pygame

# Boss enemy class
class BossEnemy:
    def __init__(self):
        self.rect = pygame.Rect(600, 500, 60, 60)
        self.attack_rect = pygame.Rect(self.rect.left - 20, self.rect.top, 20, self.rect.height)
        self.is_attacking = False
        self.attack_timer = 0

    def update(self):
        self.attack_timer += 1
        if self.attack_timer > 90:
            self.is_attacking = True
            self.attack_timer = 0
        else:
            self.is_attacking = False
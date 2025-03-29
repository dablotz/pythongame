import pygame

class Hazard:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

""" boss.py
This module contains the BossEnemy class, which represents a boss enemy in the game.
"""

import pygame

class BossEnemy: # pylint: disable=too-few-public-methods
    """ BossEnemy class representing a boss enemy in the game. """
    def __init__(self):
        """ Initialize the boss enemy with default values. """
        self.health = 5
        self.rect = pygame.Rect(600, 500, 60, 60)
        self.attack_rect = pygame.Rect(
            self.rect.left - 20, self.rect.top, 20, self.rect.height
        )
        self.is_attacking = False
        self.attack_timer = 0

    def update(self):
        """ Update the boss enemy's state. """
        self.attack_timer += 1
        if self.attack_timer > 90:
            self.is_attacking = True
            self.attack_timer = 0
        else:
            self.is_attacking = False

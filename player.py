""" 
This code defines a Player class that represents a player character in a game.
The player can move left and right, jump, and attack. 
The player is affected by gravity and has a cooldown for attacks.
"""

import pygame

class Player:
    """ Player class representing the player character. """
    def __init__(self, jump_strength=-10, gravity=0.5):
        """ Initialize the player with default values. """
        self.on_ground = True
        self.rect = pygame.Rect(100, 500, 50, 50)
        self.vel_y = 0
        self.attack_cooldown = 0
        self.attack_rect = pygame.Rect(0, 0, 0, 0)
        self.jump_strength = jump_strength
        self.gravity = gravity

    def update(self, keys):
        """ Update the player's position and state based on input keys. """
        if keys[pygame.K_LEFT]: # pylint: disable=no-member
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]: # pylint: disable=no-member
            self.rect.x += 5
        if keys[pygame.K_SPACE] and self.on_ground: # pylint: disable=no-member
            self.vel_y = self.jump_strength
            self.on_ground = False

        # Apply gravity
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # Attack
        if keys[pygame.K_z] and self.attack_cooldown == 0: # pylint: disable=no-member
            self.attack()

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def attack(self):
        """ Perform an attack. """
        self.attack_rect = pygame.Rect(
            self.rect.right, self.rect.top, 20, self.rect.height
        )
        self.attack_cooldown = 30

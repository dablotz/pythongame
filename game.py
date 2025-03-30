""" game.py
This module contains the main game loop and handles the game state, player, boss, and hazards.
"""

import sys
import pygame
from player import Player
from boss import BossEnemy
from hazard import Hazard

from game_state import GameState
from stick import draw_stick_figure

# Initialize Pygame
pygame.init() # pylint: disable=no-member

# Game settings
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 512
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -10

# Colors
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)
PURPLE = (128, 0, 128)
MAGENTA = (255, 0, 255)
GREEN = (0, 255, 0)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mini Platformer")
clock = pygame.time.Clock()

background_img = pygame.image.load("assets/Background.png").convert()
hazards_img = pygame.image.load("assets/Hazards.png").convert_alpha()
interactables_img = pygame.image.load("assets/Interactables.png").convert_alpha()

# Platforms
platforms = [
    pygame.Rect(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),
    pygame.Rect(300, 450, 200, 20),
    pygame.Rect(150, 350, 100, 20),
]

# Setup
player = Player()
player.on_ground = False
boss = BossEnemy()
hazards = [Hazard(400, SCREEN_HEIGHT - 60, 40, 20)]
game_state = GameState()

# Game loop
RUNNING = True
while RUNNING:
    clock.tick(FPS)
    screen.fill(SKY_BLUE)

    screen.blit(background_img, (0, 0))
    screen.blit(hazards_img, (0, 0))
    screen.blit(interactables_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # pylint: disable=no-member
            RUNNING = False

    keys = pygame.key.get_pressed()
    player.update(keys)
    boss.update()

    # Check collisions with platforms
    player.on_ground = False
    for platform in platforms:
        if player.rect.colliderect(platform) and player.vel_y >= 0:
            player.rect.bottom = platform.top
            player.vel_y = 0
            player.on_ground = True

    # Hazard damage
    for hazard in hazards:
        if player.rect.colliderect(hazard.rect):
            game_state.player_take_damage()

    # Player attack on boss
    if player.attack_cooldown > 25:
        if player.attack_rect.colliderect(boss.rect):
            game_state.boss_take_damage()

    # Boss attack on player
    if boss.is_attacking and boss.attack_rect.colliderect(player.rect):
        game_state.player_take_damage()

    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, (34, 139, 34), platform)

    # Draw hazards
    for hazard in hazards:
        pygame.draw.rect(screen, RED, hazard.rect)

    # Draw player
    draw_stick_figure(screen, player.rect, BLUE)
    if player.attack_cooldown > 25:
        pygame.draw.rect(screen, LIGHT_BLUE, player.attack_rect)

    # Draw boss
    draw_stick_figure(screen, boss.rect, PURPLE)
    if boss.is_attacking:
        pygame.draw.rect(screen, MAGENTA, boss.attack_rect)

    # Draw health bars
    pygame.draw.rect(screen, GREEN, (20, 20, game_state.player_health * 30, 20))
    pygame.draw.rect(screen, WHITE, (20, 20, 90, 20), 2)
    pygame.draw.rect(
        screen, RED, (SCREEN_WIDTH - 150, 20, game_state.boss_health * 30, 20)
    )
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - 150, 20, 150, 20), 2)

    # End game if over or complete
    if game_state.game_over:
        print("Game Over")
        RUNNING = False
    elif game_state.level_complete:
        print("You Win!")
        RUNNING = False

    pygame.display.flip()

pygame.quit() # pylint: disable=no-member
sys.exit()

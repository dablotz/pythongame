"""settings.py
Single source of truth for all game constants.
"""

# Display
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 512
FPS = 60
TITLE = "Mini Platformer"

# Physics (all values in pixels per second or pixels per second^2)
GRAVITY = 1800.0        # acceleration downward
JUMP_STRENGTH = -600.0  # initial vertical velocity on jump
PLAYER_SPEED = 300.0    # horizontal movement speed

# Colors
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)
PURPLE = (128, 0, 128)
MAGENTA = (255, 0, 255)
GREEN = (0, 200, 0)
FOREST_GREEN = (34, 139, 34)

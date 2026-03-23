"""enums.py
Shared enumerations used across multiple modules.

Keeping these in one place avoids circular imports between player.py,
stick.py, and renderer.py.
"""

from enum import Enum, auto


class Facing(Enum):
    """Which direction an entity is facing."""

    LEFT = auto()
    RIGHT = auto()


class PlayerState(Enum):
    """Observable player state exposed to the renderer for animation."""

    IDLE = auto()
    RUNNING = auto()
    JUMPING = auto()
    ATTACKING = auto()

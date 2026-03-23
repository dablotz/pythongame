"""scenes.py
Scene identifiers for the game's state machine.

The game moves through scenes in this order:
    TITLE -> PLAYING -> GAME_OVER | LEVEL_COMPLETE
"""

from enum import Enum, auto


class Scene(Enum):
    """All possible game screens."""

    TITLE = auto()
    PLAYING = auto()
    GAME_OVER = auto()
    LEVEL_COMPLETE = auto()

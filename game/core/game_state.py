"""
This module defines the GameState class, which manages the state of the game,
including player and boss health, and whether the game is over or the level is complete.
"""

# Seconds a character is immune to further damage after being hit.
_INVINCIBILITY_DURATION = 1.0


class GameState:
    """GameState class representing the state of the game."""

    def __init__(self):
        """Initialize the game state with default values."""
        self.player_health = 3
        self.boss_health = 5
        self.game_over = False
        self.level_complete = False
        self._player_invincibility: float = 0.0
        self._boss_invincibility: float = 0.0

    def tick(self, dt: float) -> None:
        """Advance invincibility timers by one frame.

        Args:
            dt: Elapsed time in seconds since the last frame.
        """
        if self._player_invincibility > 0:
            self._player_invincibility -= dt
        if self._boss_invincibility > 0:
            self._boss_invincibility -= dt

    def player_take_damage(self, amount=1):
        """Reduce player health by the specified amount."""
        if self._player_invincibility > 0:
            return
        self._player_invincibility = _INVINCIBILITY_DURATION
        self.player_health -= amount
        if self.player_health <= 0:
            self.player_health = 0
            self.game_over = True

    def boss_take_damage(self, amount=1):
        """Reduce boss health by the specified amount."""
        if self._boss_invincibility > 0:
            return
        self._boss_invincibility = _INVINCIBILITY_DURATION
        self.boss_health -= amount
        if self.boss_health <= 0:
            self.boss_health = 0
            self.level_complete = True

    def reset(self):
        """Reset the game state to the initial values."""
        self.player_health = 3
        self.boss_health = 5
        self.game_over = False
        self.level_complete = False
        self._player_invincibility = 0.0
        self._boss_invincibility = 0.0

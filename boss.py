"""boss.py
Boss enemy: periodic attack behaviour.

Physics (gravity, platform collision) are applied by the game loop via
physics.py — this class only handles AI-driven behaviour.
"""

import pygame

# Seconds between the start of each attack cycle.
_ATTACK_INTERVAL = 1.5
# Seconds the attack hitbox stays active each cycle.
_ATTACK_DURATION = 0.2


class BossEnemy:  # pylint: disable=too-few-public-methods
    """The boss enemy character."""

    def __init__(self, spawn: tuple[int, int] = (600, 300)) -> None:
        self._spawn = spawn
        self.rect = pygame.Rect(spawn[0], spawn[1], 60, 60)
        self.health: int = 5
        self.is_attacking: bool = False
        self._interval_timer: float = 0.0
        self._active_timer: float = 0.0
        self.attack_rect = pygame.Rect(
            self.rect.left - 20, self.rect.top, 20, self.rect.height
        )

    def update(self, dt: float) -> None:
        """Advance boss AI by one frame.

        Args:
            dt: Elapsed time in seconds since the last frame.
        """
        self._interval_timer += dt
        if self._interval_timer >= _ATTACK_INTERVAL:
            self._interval_timer = 0.0
            self._active_timer = _ATTACK_DURATION

        if self._active_timer > 0:
            self._active_timer -= dt
            self.is_attacking = True
        else:
            self.is_attacking = False

        # Keep attack rect aligned with boss position.
        self.attack_rect.topleft = (self.rect.left - 20, self.rect.top)

    def reset(self) -> None:
        """Return the boss to spawn position with cleared state."""
        self.rect.topleft = self._spawn
        self.health = 5
        self.is_attacking = False
        self._interval_timer = 0.0
        self._active_timer = 0.0
        self.attack_rect = pygame.Rect(
            self.rect.left - 20, self.rect.top, 20, self.rect.height
        )

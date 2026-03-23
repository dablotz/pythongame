"""player.py
Player character: movement, jumping, and attacking.

Physics (gravity, platform collision) are applied by the game loop via
physics.py — this class only handles player-controlled behaviour.
"""

import pygame

from game.core.enums import Facing, PlayerState
from game.core.settings import JUMP_STRENGTH, PLAYER_SPEED

# Seconds the attack hitbox stays active after pressing Z.
_ATTACK_ACTIVE_DURATION = 0.1
# Total cooldown between attacks in seconds.
_ATTACK_COOLDOWN = 0.5
# Running animation alternates leg pose at this interval (seconds).
_RUN_FRAME_INTERVAL = 0.15


class Player:  # pylint: disable=too-many-instance-attributes
    """The player character."""

    def __init__(self, spawn: tuple[int, int] = (100, 300)) -> None:
        self._spawn = spawn
        self.rect = pygame.Rect(spawn[0], spawn[1], 50, 50)
        self.vel_y: float = 0.0
        self.on_ground: bool = False
        self.facing: Facing = Facing.RIGHT
        self._attack_timer: float = 0.0
        self._anim_timer: float = 0.0
        self._is_moving: bool = False
        self.anim_frame: int = 0  # alternates 0/1 while running
        self.attack_rect = pygame.Rect(0, 0, 0, 0)
        # One-frame event flags — read by game.py to trigger sounds.
        self.just_jumped: bool = False
        self.just_attacked: bool = False

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    @property
    def is_attacking(self) -> bool:
        """True during the active hitbox window of an attack."""
        return self._attack_timer > (_ATTACK_COOLDOWN - _ATTACK_ACTIVE_DURATION)

    @property
    def state(self) -> PlayerState:
        """Current animation state for the renderer."""
        if self.is_attacking:
            return PlayerState.ATTACKING
        if not self.on_ground:
            return PlayerState.JUMPING
        if self._is_moving:
            return PlayerState.RUNNING
        return PlayerState.IDLE

    def update(self, input_handler, dt: float) -> None:
        """Apply player input. Physics are handled externally by physics.py.

        Args:
            input_handler: An InputHandler instance for the current frame.
            dt: Elapsed time in seconds since the last frame.
        """
        # Reset one-frame flags.
        self.just_jumped = False
        self.just_attacked = False

        self._is_moving = False
        if input_handler.move_left:
            self.rect.x -= int(PLAYER_SPEED * dt)
            self.facing = Facing.LEFT
            self._is_moving = True
        if input_handler.move_right:
            self.rect.x += int(PLAYER_SPEED * dt)
            self.facing = Facing.RIGHT
            self._is_moving = True

        # Running animation: cycle anim_frame between 0 and 1.
        if self._is_moving and self.on_ground:
            self._anim_timer = (self._anim_timer + dt) % (2 * _RUN_FRAME_INTERVAL)
            self.anim_frame = int(self._anim_timer >= _RUN_FRAME_INTERVAL)
        else:
            self._anim_timer = 0.0

        if input_handler.jump and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False
            self.just_jumped = True

        if input_handler.attack and self._attack_timer <= 0:
            self._start_attack()
            self.just_attacked = True

        if self._attack_timer > 0:
            self._attack_timer -= dt
            self._update_attack_rect()
        else:
            self._attack_timer = 0

    def reset(self) -> None:
        """Return the player to spawn position with cleared state."""
        self.rect.topleft = self._spawn
        self.vel_y = 0.0
        self.on_ground = False
        self.facing = Facing.RIGHT
        self._attack_timer = 0.0
        self._anim_timer = 0.0
        self._is_moving = False
        self.anim_frame = 0
        self.attack_rect = pygame.Rect(0, 0, 0, 0)
        self.just_jumped = False
        self.just_attacked = False

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _start_attack(self) -> None:
        self._attack_timer = _ATTACK_COOLDOWN
        self._update_attack_rect()

    def _update_attack_rect(self) -> None:
        """Position attack hitbox in front of the player based on facing."""
        if self.facing == Facing.RIGHT:
            self.attack_rect = pygame.Rect(
                self.rect.right, self.rect.top, 20, self.rect.height
            )
        else:
            self.attack_rect = pygame.Rect(
                self.rect.left - 20, self.rect.top, 20, self.rect.height
            )

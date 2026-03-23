"""renderer.py
Draws the game world to the screen.

All pygame.draw calls live here, keeping game logic modules free of
rendering concerns. Swap out a draw method later to add sprites without
touching player.py, boss.py, or game.py.
"""

import pygame

from assets import Assets
from enums import Facing, PlayerState
from stick import draw_stick_figure
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    RED,
    BLUE,
    LIGHT_BLUE,
    PURPLE,
    MAGENTA,
    GREEN,
    FOREST_GREEN,
    BLACK,
)


class Renderer:
    """Handles all drawing for every scene."""

    _TITLE_FONT_SIZE = 64
    _BODY_FONT_SIZE = 32
    _HUD_FONT_SIZE = 24

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self._title_font = pygame.font.Font(None, self._TITLE_FONT_SIZE)
        self._body_font = pygame.font.Font(None, self._BODY_FONT_SIZE)
        self._hud_font = pygame.font.Font(None, self._HUD_FONT_SIZE)

    # ------------------------------------------------------------------
    # Scene entry points
    # ------------------------------------------------------------------

    def draw_title(self) -> None:
        """Title / start screen."""
        self.screen.fill(BLACK)
        self._centered_text("Mini Platformer", self._title_font, WHITE, y_ratio=0.35)
        self._centered_text(
            "Press SPACE or Z to start", self._body_font, GREEN, y_ratio=0.55
        )
        self._centered_text(
            "Arrow keys to move  |  Space to jump  |  Z to attack",
            self._hud_font,
            WHITE,
            y_ratio=0.70,
        )

    def draw_playing(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        player,
        boss,
        game_state,
        platforms: list[pygame.Rect],
        hazards: list,
    ) -> None:
        """Main gameplay screen."""
        # Background layers from LDtk export
        self.screen.blit(Assets.background("assets/Background.png"), (0, 0))
        self.screen.blit(Assets.image("assets/Hazards.png"), (0, 0))
        self.screen.blit(Assets.image("assets/Interactables.png"), (0, 0))

        # Platforms
        for platform in platforms:
            pygame.draw.rect(self.screen, FOREST_GREEN, platform)

        # Hazards
        for hazard in hazards:
            pygame.draw.rect(self.screen, RED, hazard.rect)

        # Player — pass state and facing for animated pose
        draw_stick_figure(
            self.screen,
            player.rect,
            BLUE,
            facing=player.facing,
            state=player.state,
            anim_frame=player.anim_frame,
        )
        if player.is_attacking:
            pygame.draw.rect(self.screen, LIGHT_BLUE, player.attack_rect)

        # Boss — static pose (boss AI doesn't have a facing concept yet)
        draw_stick_figure(
            self.screen,
            boss.rect,
            PURPLE,
            facing=Facing.LEFT,
            state=PlayerState.ATTACKING if boss.is_attacking else PlayerState.IDLE,
        )
        if boss.is_attacking:
            pygame.draw.rect(self.screen, MAGENTA, boss.attack_rect)

        # HUD — health bars
        self._draw_health_bars(game_state)

    def draw_game_over(self) -> None:
        """Game over screen (player lost)."""
        self.screen.fill(BLACK)
        self._centered_text("Game Over", self._title_font, RED, y_ratio=0.30)
        self._centered_text("Better luck next time!", self._body_font, WHITE, y_ratio=0.50)
        self._centered_text(
            "Press SPACE or Z to try again", self._hud_font, GREEN, y_ratio=0.68
        )

    def draw_level_complete(self) -> None:
        """Victory screen."""
        self.screen.fill(BLACK)
        self._centered_text("You Win!", self._title_font, GREEN, y_ratio=0.30)
        self._centered_text("The boss has been defeated!", self._body_font, WHITE, y_ratio=0.50)
        self._centered_text(
            "Press SPACE or Z to play again", self._hud_font, GREEN, y_ratio=0.68
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _draw_health_bars(self, game_state) -> None:
        player_bar_w = game_state.player_health * 30
        boss_bar_w = game_state.boss_health * 30

        # Player health (left side)
        pygame.draw.rect(self.screen, GREEN, (20, 20, player_bar_w, 20))
        pygame.draw.rect(self.screen, WHITE, (20, 20, 90, 20), 2)

        # Boss health (right side)
        boss_bar_x = SCREEN_WIDTH - 20 - boss_bar_w
        pygame.draw.rect(self.screen, RED, (boss_bar_x, 20, boss_bar_w, 20))
        pygame.draw.rect(self.screen, WHITE, (SCREEN_WIDTH - 170, 20, 150, 20), 2)

    def _centered_text(
        self,
        text: str,
        font: pygame.font.Font,
        color: tuple,
        y_ratio: float,
    ) -> None:
        surface = font.render(text, True, color)
        rect = surface.get_rect(
            center=(SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * y_ratio))
        )
        self.screen.blit(surface, rect)

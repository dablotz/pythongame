"""main.py
Initialises pygame, owns the scene state machine, and runs the main loop.

The loop itself is intentionally thin:
  - InputHandler reads raw input once per frame.
  - Entity update methods interpret that input.
  - physics.py applies gravity and resolves collisions.
  - Renderer draws the current scene.
"""

import sys

import pygame  # pylint: disable=no-member

from game.rendering.assets import Assets
from game.entities.boss import BossEnemy
from game.core.game_state import GameState
from game.core.input_handler import InputHandler
from game.levels.level import LevelData
from game.core.physics import apply_gravity, resolve_platform_collisions
from game.entities.player import Player
from game.rendering.renderer import Renderer
from game.core.scenes import Scene
from game.core.settings import FPS, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE
from game.audio.sounds import Sounds

_LEVEL_PATH = "assets/data.json"


def _update_playing(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    player, boss, game_state, level, input_handler, dt
):
    """Run one frame of gameplay logic. Returns (player_hp_delta, boss_hp_delta)."""
    prev_player_hp = game_state.player_health
    prev_boss_hp = game_state.boss_health

    game_state.tick(dt)
    player.update(input_handler, dt)
    boss.update(dt)

    apply_gravity(player, dt)
    player.on_ground = resolve_platform_collisions(player, level.platforms)

    apply_gravity(boss, dt)
    boss.on_ground = resolve_platform_collisions(boss, level.platforms)

    for hazard in level.hazards:
        if player.rect.colliderect(hazard.rect):
            game_state.player_take_damage()

    if player.is_attacking and player.attack_rect.colliderect(boss.rect):
        game_state.boss_take_damage()

    if boss.is_attacking and boss.attack_rect.colliderect(player.rect):
        game_state.player_take_damage()

    return game_state.player_health - prev_player_hp, game_state.boss_health - prev_boss_hp


def _play_frame_sounds(player, player_hp_delta, boss_hp_delta):
    """Fire sounds for events that happened this frame."""
    if player.just_jumped:
        Sounds.play_jump()
    if player.just_attacked:
        Sounds.play_attack()
    if player_hp_delta < 0:
        Sounds.play_player_hit()
    if boss_hp_delta < 0:
        Sounds.play_boss_hit()


def _restart(player, boss, game_state):
    """Reset all game objects for a new run."""
    player.reset()
    boss.reset()
    game_state.reset()


def main() -> None:  # pylint: disable=too-many-branches,too-many-statements
    """Initialise pygame and run the game loop."""
    pygame.init()  # pylint: disable=no-member
    Sounds.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # pylint: disable=no-member
    pygame.display.set_caption(TITLE)  # pylint: disable=no-member
    clock = pygame.time.Clock()  # pylint: disable=no-member

    renderer = Renderer(screen)
    input_handler = InputHandler()

    level = LevelData(_LEVEL_PATH)

    # Pre-load shared assets so the first frame doesn't hitch.
    Assets.background("assets/Background.png")
    Assets.image("assets/Hazards.png")
    Assets.image("assets/Interactables.png")

    player = Player(spawn=level.player_spawn)
    boss = BossEnemy(spawn=level.boss_spawn)
    game_state = GameState()

    scene = Scene.TITLE
    end_sound_played = False

    while True:
        dt = clock.tick(FPS) / 1000.0
        input_handler.process()

        if input_handler.quit:
            break

        # ---- Title scene ------------------------------------------------
        if scene == Scene.TITLE:
            renderer.draw_title()
            if input_handler.jump or input_handler.attack:
                scene = Scene.PLAYING

        # ---- Playing scene ----------------------------------------------
        elif scene == Scene.PLAYING:
            player_hp_delta, boss_hp_delta = _update_playing(
                player, boss, game_state, level, input_handler, dt
            )
            _play_frame_sounds(player, player_hp_delta, boss_hp_delta)
            renderer.draw_playing(
                player, boss, game_state, level.platforms, level.hazards
            )

            if game_state.game_over:
                scene = Scene.GAME_OVER
                end_sound_played = False
            elif game_state.level_complete:
                scene = Scene.LEVEL_COMPLETE
                end_sound_played = False

        # ---- End screens ------------------------------------------------
        elif scene == Scene.GAME_OVER:
            if not end_sound_played:
                Sounds.play_game_over()
                end_sound_played = True
            renderer.draw_game_over()
            if input_handler.jump or input_handler.attack:
                _restart(player, boss, game_state)
                scene = Scene.PLAYING

        elif scene == Scene.LEVEL_COMPLETE:
            if not end_sound_played:
                Sounds.play_victory()
                end_sound_played = True
            renderer.draw_level_complete()
            if input_handler.jump or input_handler.attack:
                _restart(player, boss, game_state)
                scene = Scene.PLAYING

        pygame.display.flip()  # pylint: disable=no-member

    pygame.quit()  # pylint: disable=no-member
    sys.exit()

"""stick.py
Stick figure renderer with state and facing awareness.

This is intentionally the only file that needs to change when swapping
stick figures for real sprites — the renderer will call the same function
with the same arguments, just getting pixel art back instead of lines.
"""

import pygame

from game.core.enums import Facing, PlayerState


def draw_stick_figure(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    screen: pygame.Surface,
    rect: pygame.Rect,
    color: tuple,
    facing: Facing = Facing.RIGHT,
    state: PlayerState = PlayerState.IDLE,
    anim_frame: int = 0,
) -> None:
    """Draw a stick figure that reflects the entity's current state.

    Args:
        screen:     Surface to draw on.
        rect:       Bounding rect of the entity.
        color:      Line/circle colour.
        facing:     LEFT or RIGHT — controls which side the attack arm swings.
        state:      Current PlayerState — controls pose.
        anim_frame: Alternates 0/1 while running to animate legs.
    """
    head_radius = rect.width // 4
    head_center = (rect.centerx, rect.top + head_radius)
    body_top = (rect.centerx, rect.top + 2 * head_radius)
    body_bottom = (rect.centerx, rect.bottom - rect.height // 4)

    # Head
    pygame.draw.circle(screen, color, head_center, head_radius, 2)

    # Body
    pygame.draw.line(screen, color, body_top, body_bottom, 2)

    # Arms — position depends on state and facing
    _draw_arms(screen, rect, color, facing, state)

    # Legs — pose depends on state and anim_frame
    _draw_legs(screen, rect, color, body_bottom, state, anim_frame)


def _draw_arms(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    screen: pygame.Surface,
    rect: pygame.Rect,
    color: tuple,
    facing: Facing,
    state: PlayerState,
) -> None:
    arm_y = rect.top + rect.height // 2

    if state == PlayerState.ATTACKING:
        # Lead arm extends forward, trailing arm stays back.
        if facing == Facing.RIGHT:
            pygame.draw.line(screen, color, (rect.centerx, arm_y), (rect.right + 8, arm_y - 6), 2)
            pygame.draw.line(screen, color, (rect.centerx, arm_y), (rect.left + 6, arm_y + 4), 2)
        else:
            pygame.draw.line(screen, color, (rect.centerx, arm_y), (rect.left - 8, arm_y - 6), 2)
            pygame.draw.line(screen, color, (rect.centerx, arm_y), (rect.right - 6, arm_y + 4), 2)
    elif state == PlayerState.JUMPING:
        # Arms raised for balance.
        pygame.draw.line(screen, color, (rect.centerx, arm_y), (rect.left, arm_y - 8), 2)
        pygame.draw.line(screen, color, (rect.centerx, arm_y), (rect.right, arm_y - 8), 2)
    else:
        # Idle / running: standard horizontal arms.
        pygame.draw.line(screen, color, (rect.left + 5, arm_y), (rect.right - 5, arm_y), 2)


def _draw_legs(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    screen: pygame.Surface,
    rect: pygame.Rect,
    color: tuple,
    body_bottom: tuple,
    state: PlayerState,
    anim_frame: int,
) -> None:
    if state == PlayerState.JUMPING:
        # Legs tucked — both point straight down.
        pygame.draw.line(screen, color, body_bottom, (rect.centerx - 6, rect.bottom), 2)
        pygame.draw.line(screen, color, body_bottom, (rect.centerx + 6, rect.bottom), 2)
    elif state == PlayerState.RUNNING and anim_frame == 1:
        # Alternate leg pose: front and back legs swap.
        pygame.draw.line(screen, color, body_bottom, (rect.right - 4, rect.bottom), 2)
        pygame.draw.line(screen, color, body_bottom, (rect.left + 4, rect.bottom), 2)
    else:
        # Default: legs spread to corners.
        pygame.draw.line(screen, color, body_bottom, (rect.left + 10, rect.bottom), 2)
        pygame.draw.line(screen, color, body_bottom, (rect.right - 10, rect.bottom), 2)

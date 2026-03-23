"""physics.py
Stateless helpers for vertical physics and platform collision.

Keeping physics separate from entities means:
- Entities don't need to know about each other or the world layout.
- Physics behaviour is easy to test in isolation.
- Delta-time values are applied in one place, so changing gravity or speed
  only requires editing settings.py.
"""

import pygame

from game.core.settings import GRAVITY


def apply_gravity(entity, dt: float) -> None:
    """Accelerate entity downward and advance its vertical position.

    Args:
        entity: Any object with a ``vel_y`` float and a ``pygame.Rect`` rect.
        dt: Elapsed time in seconds since the last frame.
    """
    entity.vel_y += GRAVITY * dt
    entity.rect.y += int(entity.vel_y * dt)


def resolve_platform_collisions(
    entity, platforms: list[pygame.Rect]
) -> bool:
    """Snap entity to the top of any platform it has fallen into.

    Only resolves downward collisions (entity moving toward the platform),
    which prevents sticking to ceilings when jumping into them from below.

    Args:
        entity: Any object with a ``vel_y`` float, ``on_ground`` bool,
                and a ``pygame.Rect`` rect.
        platforms: List of platform rects to test against.

    Returns:
        True if the entity is resting on a platform, False otherwise.
    """
    on_ground = False
    for platform in platforms:
        if entity.rect.colliderect(platform) and entity.vel_y >= 0:
            entity.rect.bottom = platform.top
            entity.vel_y = 0
            on_ground = True
    return on_ground

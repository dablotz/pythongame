"""Tests for physics helpers."""
# pylint: disable=missing-function-docstring,redefined-outer-name

import pygame
import pytest
from game.core.physics import apply_gravity, resolve_platform_collisions
from game.core.settings import GRAVITY


class _Entity:  # pylint: disable=too-few-public-methods
    """Minimal stand-in for Player or BossEnemy used in physics tests."""

    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.vel_y: float = 0.0
        self.on_ground: bool = False


@pytest.fixture
def entity():
    return _Entity(0, 0, 50, 50)


# ---- apply_gravity -------------------------------------------------------


def test_gravity_increases_vel_y(entity):
    apply_gravity(entity, dt=1.0)
    assert entity.vel_y == pytest.approx(GRAVITY)


def test_gravity_moves_entity_downward(entity):
    apply_gravity(entity, dt=1.0)
    assert entity.rect.y > 0


def test_gravity_accumulates_over_frames(entity):
    apply_gravity(entity, dt=0.5)
    apply_gravity(entity, dt=0.5)
    assert entity.vel_y == pytest.approx(GRAVITY)


# ---- resolve_platform_collisions -----------------------------------------


def test_entity_lands_on_platform():
    # Entity falling into a platform from above.
    e = _Entity(0, 90, 50, 50)  # bottom at 140
    e.vel_y = 10.0
    platform = pygame.Rect(0, 100, 200, 20)  # top at 100
    on_ground = resolve_platform_collisions(e, [platform])
    assert on_ground
    assert e.rect.bottom == platform.top
    assert e.vel_y == 0


def test_no_collision_when_entity_above_platform():
    e = _Entity(0, 0, 50, 50)  # bottom at 50, well above platform
    e.vel_y = 0.0
    platform = pygame.Rect(0, 200, 200, 20)
    on_ground = resolve_platform_collisions(e, [platform])
    assert not on_ground


def test_no_snap_when_moving_upward():
    # Entity clipping into a platform while moving upward (jumping through).
    e = _Entity(0, 90, 50, 50)
    e.vel_y = -10.0  # moving up
    platform = pygame.Rect(0, 100, 200, 20)
    on_ground = resolve_platform_collisions(e, [platform])
    assert not on_ground
    assert e.vel_y == -10.0  # unchanged

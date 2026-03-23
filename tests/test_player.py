"""Tests for Player state, facing, and reset."""
# pylint: disable=missing-function-docstring,redefined-outer-name
import pytest
from game.core.enums import Facing, PlayerState
from game.entities.player import Player


class _Input:  # pylint: disable=too-few-public-methods
    """Minimal InputHandler stand-in."""

    def __init__(self, left=False, right=False, jump=False, attack=False):
        self.move_left = left
        self.move_right = right
        self.jump = jump
        self.attack = attack
        self.quit = False


@pytest.fixture
def player():
    return Player(spawn=(100, 300))


def test_initial_state(player):
    # Player starts airborne; physics will land them on the first frame.
    assert player.facing == Facing.RIGHT
    assert not player.is_attacking
    assert player.state == PlayerState.JUMPING


def test_facing_updates_on_move_left(player):
    player.on_ground = True
    player.update(_Input(left=True), dt=0.016)
    assert player.facing == Facing.LEFT


def test_facing_updates_on_move_right(player):
    player.on_ground = True
    player.facing = Facing.LEFT
    player.update(_Input(right=True), dt=0.016)
    assert player.facing == Facing.RIGHT


def test_state_running_when_moving_on_ground(player):
    player.on_ground = True
    # Need enough elapsed time to register as running.
    player.update(_Input(right=True), dt=0.2)
    assert player.state == PlayerState.RUNNING


def test_state_jumping_when_airborne(player):
    player.on_ground = False
    player.update(_Input(), dt=0.016)
    assert player.state == PlayerState.JUMPING


def test_state_attacking(player):
    player.on_ground = True
    player.update(_Input(attack=True), dt=0.016)
    assert player.state == PlayerState.ATTACKING


def test_attack_rect_right_of_player_when_facing_right(player):
    player.on_ground = True
    player.update(_Input(attack=True), dt=0.016)
    assert player.attack_rect.left == player.rect.right


def test_attack_rect_left_of_player_when_facing_left(player):
    player.on_ground = True
    player.facing = Facing.LEFT
    player.update(_Input(attack=True), dt=0.016)
    assert player.attack_rect.right == player.rect.left


def test_just_jumped_flag(player):
    player.on_ground = True
    player.update(_Input(jump=True), dt=0.016)
    assert player.just_jumped


def test_just_jumped_resets_next_frame(player):
    player.on_ground = True
    player.update(_Input(jump=True), dt=0.016)
    player.on_ground = True  # pretend physics reset it
    player.update(_Input(), dt=0.016)
    assert not player.just_jumped


def test_just_attacked_flag(player):
    player.on_ground = True
    player.update(_Input(attack=True), dt=0.016)
    assert player.just_attacked


def test_reset_returns_to_spawn(player):
    player.rect.topleft = (999, 999)
    player.vel_y = -300
    player.facing = Facing.LEFT
    player.reset()
    assert player.rect.topleft == (100, 300)
    assert player.vel_y == 0.0
    assert player.facing == Facing.RIGHT
    assert not player.is_attacking
    assert not player.just_jumped

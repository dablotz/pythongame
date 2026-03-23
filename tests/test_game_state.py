"""Tests for GameState — no pygame required."""
# pylint: disable=missing-function-docstring,redefined-outer-name

import pytest
from game_state import GameState


@pytest.fixture
def state():
    return GameState()


def test_initial_values(state):
    assert state.player_health == 3
    assert state.boss_health == 5
    assert not state.game_over
    assert not state.level_complete


def test_player_take_damage_decrements_health(state):
    state.player_take_damage()
    assert state.player_health == 2
    assert not state.game_over


def test_player_health_floored_at_zero(state):
    state.player_take_damage(100)
    assert state.player_health == 0


def test_game_over_when_player_health_reaches_zero(state):
    state.player_take_damage(3)
    assert state.game_over


def test_boss_take_damage_decrements_health(state):
    state.boss_take_damage()
    assert state.boss_health == 4
    assert not state.level_complete


def test_level_complete_when_boss_health_reaches_zero(state):
    state.boss_take_damage(5)
    assert state.boss_health == 0
    assert state.level_complete


def test_reset_restores_initial_state(state):
    state.player_take_damage(3)
    state.boss_take_damage(5)
    state.reset()
    assert state.player_health == 3
    assert state.boss_health == 5
    assert not state.game_over
    assert not state.level_complete

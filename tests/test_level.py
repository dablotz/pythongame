"""Tests for the LevelData loader."""
# pylint: disable=missing-function-docstring,redefined-outer-name
import json
import os
import tempfile

import pytest
from level import LevelData


@pytest.fixture
def level_file():
    """Write a minimal level JSON to a temp file and return its path."""
    data = {
        "width": 1024,
        "height": 512,
        "layers": ["Background.png"],
        "platforms": [
            {"x": 0, "y": 472, "w": 1024, "h": 40},
            {"x": 300, "y": 380, "w": 200, "h": 20},
        ],
        "hazards": [
            {"x": 400, "y": 452, "w": 40, "h": 20}
        ],
        "entities": {
            "player_spawn": {"x": 100, "y": 300},
            "boss_spawn": {"x": 600, "y": 300},
        },
    }
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as f:
        json.dump(data, f)
        return f.name


@pytest.fixture(autouse=True)
def cleanup(level_file):
    yield
    os.unlink(level_file)


def test_dimensions(level_file):
    level = LevelData(level_file)
    assert level.width == 1024
    assert level.height == 512


def test_platforms_loaded(level_file):
    level = LevelData(level_file)
    assert len(level.platforms) == 2
    assert level.platforms[0].x == 0
    assert level.platforms[0].y == 472


def test_hazards_loaded(level_file):
    level = LevelData(level_file)
    assert len(level.hazards) == 1
    assert level.hazards[0].rect.x == 400


def test_player_spawn(level_file):
    level = LevelData(level_file)
    assert level.player_spawn == (100, 300)


def test_boss_spawn(level_file):
    level = LevelData(level_file)
    assert level.boss_spawn == (600, 300)


def test_missing_optional_keys():
    """Level with only required keys should use sensible defaults."""
    data = {"width": 512, "height": 256, "layers": []}
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    ) as f:
        json.dump(data, f)
        path = f.name
    try:
        level = LevelData(path)
        assert level.platforms == []
        assert level.hazards == []
        assert level.player_spawn == (100, 300)
        assert level.boss_spawn == (600, 300)
    finally:
        os.unlink(path)

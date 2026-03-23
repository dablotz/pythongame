"""level.py
Loads level geometry and entity spawn positions from the JSON file that
sits alongside the LDtk-exported assets.

Adding a new level only requires:
  1. Exporting new PNG layers from LDtk.
  2. Creating a matching JSON file with platforms, hazards, and entity spawns.
  3. Passing the new path to LevelData().
"""

import json

import pygame

from hazard import Hazard


class LevelData:  # pylint: disable=too-few-public-methods
    """All geometry and metadata for a single level."""

    def __init__(self, path: str) -> None:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        self.width: int = data["width"]
        self.height: int = data["height"]
        self.layers: list[str] = data["layers"]

        self.platforms: list[pygame.Rect] = [
            pygame.Rect(p["x"], p["y"], p["w"], p["h"])
            for p in data.get("platforms", [])
        ]

        self.hazards: list[Hazard] = [
            Hazard(h["x"], h["y"], h["w"], h["h"])
            for h in data.get("hazards", [])
        ]

        entities = data.get("entities", {})
        player_spawn = entities.get("player_spawn", {"x": 100, "y": 300})
        boss_spawn = entities.get("boss_spawn", {"x": 600, "y": 300})

        self.player_spawn: tuple[int, int] = (player_spawn["x"], player_spawn["y"])
        self.boss_spawn: tuple[int, int] = (boss_spawn["x"], boss_spawn["y"])

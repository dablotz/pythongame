"""assets.py
Asset manager — loads images and sounds once and caches them.
Call Assets.image() or Assets.background() instead of pygame.image.load() directly.
"""

import pygame


class Assets:
    """Lazy-loading cache for game assets. All methods are class-level."""

    _cache: dict[str, pygame.Surface] = {}

    @classmethod
    def image(cls, path: str) -> pygame.Surface:
        """Load an image with alpha channel, or return the cached copy."""
        if path not in cls._cache:
            cls._cache[path] = pygame.image.load(path).convert_alpha()
        return cls._cache[path]

    @classmethod
    def background(cls, path: str) -> pygame.Surface:
        """Load an opaque background image, or return the cached copy."""
        if path not in cls._cache:
            cls._cache[path] = pygame.image.load(path).convert()
        return cls._cache[path]

    @classmethod
    def clear(cls) -> None:
        """Release all cached surfaces (useful between levels or in tests)."""
        cls._cache.clear()

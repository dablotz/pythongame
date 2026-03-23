"""conftest.py
Session-wide pytest fixtures.

SDL is pointed at dummy drivers so pygame can initialise without a real
display or audio device — works in headless CI environments too.
"""

import os

import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame  # noqa: E402  pylint: disable=wrong-import-position


@pytest.fixture(scope="session", autouse=True)
def pygame_session():
    """Initialise pygame once for the whole test session, then shut it down."""
    pygame.init()  # pylint: disable=no-member
    yield
    pygame.quit()  # pylint: disable=no-member

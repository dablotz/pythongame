"""input_handler.py
Translates raw pygame events into named game actions.

Entities receive an InputHandler rather than raw key state, which means:
- Rebinding a key only requires changing this file.
- Entities don't import pygame directly for input.
- Input is easy to mock or replay in tests.
"""

import pygame


class InputHandler:  # pylint: disable=too-few-public-methods
    """Collects and exposes player input for a single frame."""

    def __init__(self) -> None:
        self.quit = False
        self.move_left = False
        self.move_right = False
        # Jump and attack are True only on the frame the key was first pressed,
        # preventing hold-to-spam behaviour.
        self.jump = False
        self.attack = False

    def process(self) -> None:
        """Read pygame events and held keys. Call once per frame."""
        self.jump = False
        self.attack = False

        for event in pygame.event.get():  # pylint: disable=no-member
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                self.quit = True
            elif event.type == pygame.KEYDOWN:  # pylint: disable=no-member
                if event.key == pygame.K_SPACE:  # pylint: disable=no-member
                    self.jump = True
                if event.key == pygame.K_z:  # pylint: disable=no-member
                    self.attack = True

        keys = pygame.key.get_pressed()
        self.move_left = bool(keys[pygame.K_LEFT])  # pylint: disable=no-member
        self.move_right = bool(keys[pygame.K_RIGHT])  # pylint: disable=no-member

"""input_handler.py
Translates raw pygame events into named game actions.

Entities receive an InputHandler rather than raw key state, which means:
- Rebinding a key only requires changing this file.
- Entities don't import pygame directly for input.
- Input is easy to mock or replay in tests.

Controller mapping (Xbox / standard HID layout):
  Left stick / D-pad left|right  → move
  Button 0  (A / Cross)          → jump
  Button 1  (B / Circle)         → attack
  Button 2  (X / Square)         → attack (alternate)
  Button 7  (Start)              → quit (title screen)
"""

import pygame

# Analogue stick dead zone — values below this are treated as neutral.
_AXIS_DEAD_ZONE = 0.3


class InputHandler:  # pylint: disable=too-few-public-methods
    """Collects and exposes player input for a single frame."""

    def __init__(self) -> None:
        self.quit = False
        self.move_left = False
        self.move_right = False
        # Jump and attack are True only on the frame the key/button was first
        # pressed, preventing hold-to-spam behaviour.
        self.jump = False
        self.attack = False

        self._joystick: pygame.joystick.JoystickType | None = None
        self._connect_joystick()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def process(self) -> None:  # pylint: disable=too-many-branches
        """Read pygame events and held keys/axes. Call once per frame."""
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
                if event.key == pygame.K_q:  # pylint: disable=no-member
                    self.quit = True

            elif event.type == pygame.JOYBUTTONDOWN:  # pylint: disable=no-member
                if event.button == 0:                    # A / Cross
                    self.jump = True
                elif event.button in (1, 2):             # B|X / Circle|Square
                    self.attack = True
                elif event.button == 7:                  # Start
                    self.quit = True

            elif event.type == pygame.JOYDEVICEADDED:   # pylint: disable=no-member
                self._connect_joystick()
            elif event.type == pygame.JOYDEVICEREMOVED:  # pylint: disable=no-member
                self._joystick = None

        # Keyboard held-key movement
        keys = pygame.key.get_pressed()
        self.move_left = bool(keys[pygame.K_LEFT])   # pylint: disable=no-member
        self.move_right = bool(keys[pygame.K_RIGHT])  # pylint: disable=no-member

        # Controller movement — OR with keyboard so either device works
        if self._joystick is not None:
            axis_x = self._joystick.get_axis(0)
            hat_x = self._joystick.get_hat(0)[0] if self._joystick.get_numhats() > 0 else 0
            self.move_left = self.move_left or axis_x < -_AXIS_DEAD_ZONE or hat_x < 0
            self.move_right = self.move_right or axis_x > _AXIS_DEAD_ZONE or hat_x > 0

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _connect_joystick(self) -> None:
        """Initialise the first available joystick, if any."""
        pygame.joystick.init()  # pylint: disable=no-member
        if pygame.joystick.get_count() > 0:  # pylint: disable=no-member
            self._joystick = pygame.joystick.Joystick(0)  # pylint: disable=no-member
            self._joystick.init()

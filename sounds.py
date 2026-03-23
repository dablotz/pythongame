"""sounds.py
Programmatic sound effects — no audio files required.

All sounds are generated as simple square waves at startup via
pygame.mixer. Call Sounds.init() once after pygame.init(), then use the
play_* class methods anywhere in the game.

When your kid creates real sound effects, replace the _make_tone() call
for that sound with Assets-style loading from a file instead.
"""

import array
import math

import pygame


def _make_tone(
    frequency: int,
    duration_ms: int,
    volume: float = 0.15,
    sample_rate: int = 22050,
) -> pygame.mixer.Sound:
    """Generate a square-wave tone and return it as a pygame Sound.

    Args:
        frequency:   Pitch in Hz.
        duration_ms: Length in milliseconds.
        volume:      Amplitude in range [0.0, 1.0].
        sample_rate: Samples per second (must match mixer init).
    """
    n_samples = int(sample_rate * duration_ms / 1000)
    buf = array.array("h")
    period = sample_rate / frequency
    peak = int(32767 * volume)

    for i in range(n_samples):
        buf.append(peak if (i % period) < (period / 2) else -peak)

    # Short linear fade-out to avoid a click at the end.
    fade = min(int(sample_rate * 0.01), n_samples)
    for i in range(fade):
        scale = 1.0 - (i / fade)
        buf[n_samples - fade + i] = int(buf[n_samples - fade + i] * scale)

    return pygame.mixer.Sound(buffer=buf)


def _make_slide(
    freq_start: int,
    freq_end: int,
    duration_ms: int,
    volume: float = 0.15,
    sample_rate: int = 22050,
) -> pygame.mixer.Sound:
    """Generate a frequency-sliding square wave (pitch bend effect)."""
    n_samples = int(sample_rate * duration_ms / 1000)
    buf = array.array("h")
    peak = int(32767 * volume)
    phase = 0.0

    for i in range(n_samples):
        t = i / n_samples
        freq = freq_start + (freq_end - freq_start) * t
        phase += freq / sample_rate
        buf.append(peak if math.fmod(phase, 1.0) < 0.5 else -peak)

    fade = min(int(sample_rate * 0.01), n_samples)
    for i in range(fade):
        scale = 1.0 - (i / fade)
        buf[n_samples - fade + i] = int(buf[n_samples - fade + i] * scale)

    return pygame.mixer.Sound(buffer=buf)


class Sounds:
    """Cached sound effects. Call Sounds.init() once at startup."""

    _jump: pygame.mixer.Sound | None = None
    _attack: pygame.mixer.Sound | None = None
    _player_hit: pygame.mixer.Sound | None = None
    _boss_hit: pygame.mixer.Sound | None = None
    _game_over: pygame.mixer.Sound | None = None
    _victory: pygame.mixer.Sound | None = None

    @classmethod
    def init(cls) -> None:
        """Generate all sounds. Must be called after pygame.init()."""
        pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)  # pylint: disable=no-member
        cls._jump = _make_slide(300, 600, 120)       # upward chirp
        cls._attack = _make_tone(500, 60, volume=0.2)  # sharp crack
        cls._player_hit = _make_slide(200, 80, 250)  # downward thud
        cls._boss_hit = _make_tone(350, 100)          # solid hit
        cls._game_over = _make_slide(300, 80, 700)   # slow descending tone
        cls._victory = _make_slide(400, 900, 400)    # rising fanfare

    @classmethod
    def play_jump(cls) -> None:
        """Play when the player jumps."""
        if cls._jump:
            cls._jump.play()

    @classmethod
    def play_attack(cls) -> None:
        """Play when the player swings."""
        if cls._attack:
            cls._attack.play()

    @classmethod
    def play_player_hit(cls) -> None:
        """Play when the player takes damage."""
        if cls._player_hit:
            cls._player_hit.play()

    @classmethod
    def play_boss_hit(cls) -> None:
        """Play when the boss takes damage."""
        if cls._boss_hit:
            cls._boss_hit.play()

    @classmethod
    def play_game_over(cls) -> None:
        """Play on the game over screen."""
        if cls._game_over:
            cls._game_over.play()

    @classmethod
    def play_victory(cls) -> None:
        """Play on the level complete screen."""
        if cls._victory:
            cls._victory.play()

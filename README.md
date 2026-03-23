# pythongame

A 2D platformer built with the help of my kiddo. Fight the boss, avoid hazards, and eventually play with art drawn by hand.

## Running the game

```bash
make venv
source .venv/bin/activate
python run.py
# or
python -m game
```

## Controls

See [GAMEPLAY.md](GAMEPLAY.md) for controls and win/loss conditions.

## Project structure

```
game/
├── audio/       — sound effects
├── core/        — settings, physics, input, game state, enums, scenes
├── entities/    — player, boss, hazard
├── levels/      — level data loader (reads assets/data.json)
└── rendering/   — renderer, asset cache, stick figure drawing
assets/          — LDtk-exported PNG layers and level JSON
tests/           — pytest test suite
run.py           — entry point
```

## Development

```bash
make venv          # create .venv and install dependencies (first time)
make test          # run the test suite
make lint          # pylint
make format        # black (rewrites files)
make check-format  # black --check (read-only, used in CI)
make all           # install → format → lint → test
```

## Built with

- [pygame](https://github.com/pygame/pygame) — game loop, rendering, input, audio
- [LDtk](https://github.com/deepnight/ldtk) — level and asset design

## Goals

- Learning pygame and LDtk
- Collaborating alongside an LLM
- Building a game together with my kid — they'll eventually draw all the art

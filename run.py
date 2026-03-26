"""run.py
Launches the game. Run from the project root:

    python run.py
    python -m game
"""

import asyncio

from game.main import main

if __name__ == "__main__":
    asyncio.run(main())

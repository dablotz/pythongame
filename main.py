"""main.py
Pygbag entry point — required at the project root for web builds.

Build and serve locally:  python -m pygbag .
Build only:               python -m pygbag --build .
Output lands in:          build/web/
"""

import asyncio

from game.main import main

asyncio.run(main())

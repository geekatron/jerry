"""CLI Package Entry Point.

This module enables running the CLI package as a Python module:

    python -m src.interface.cli

This avoids the RuntimeWarning that occurs when running:

    python -m src.interface.cli.main

The warning occurred because __init__.py imports from main.py, causing
main to be loaded as a regular module before -m tries to run it as __main__.

References:
    - DISC-017: RuntimeWarning When Running CLI with -m Flag
    - https://docs.python.org/3/library/__main__.html
"""

from src.interface.cli.main import main

if __name__ == "__main__":
    main()

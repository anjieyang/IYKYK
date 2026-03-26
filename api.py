"""Compatibility shim for the local comparison demo.

Core runtime entrypoints live under the ``uncommon_route`` package.
The actual demo server implementation now lives in ``demo.compare_api``.
"""

from demo.compare_api import app, main

__all__ = ["app", "main"]


if __name__ == "__main__":
    main()

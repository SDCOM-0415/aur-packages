#!/usr/bin/env python3
"""
AUR包更新工具主入口
"""

from cli.cli import update_main
import asyncio

if __name__ == "__main__":
    asyncio.run(update_main())

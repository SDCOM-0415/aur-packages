#!/usr/bin/env python3
"""AUR 包自动更新工具主入口"""

import argparse
import asyncio
import sys

from core.package_updater import PackageUpdater


async def main() -> None:
    """主函数，处理命令行参数并执行相应操作"""
    parser = argparse.ArgumentParser(description="AUR包更新工具")
    parser.add_argument("--package", "-p", help="更新指定的包")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有可用的包")
    parser.add_argument("--all", "-a", action="store_true", help="更新所有包")

    args = parser.parse_args()

    updater = PackageUpdater()

    if args.list:
        updater.list_available_packages()
        return

    if args.package:
        success = await updater.update_single_package(args.package)
        sys.exit(0 if success else 1)
    else:
        # 默认行为：更新所有包
        await updater.update_all_packages()


if __name__ == "__main__":
    asyncio.run(main())

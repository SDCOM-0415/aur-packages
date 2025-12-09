import argparse
import sys
from core.package_updater import PackageUpdater


async def update_main():
    """主函数，使用argparse处理命令行参数"""
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
    elif args.all:
        await updater.update_all_packages()
    else:
        # 默认行为：更新所有包
        await updater.update_all_packages()

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个 Arch Linux AUR 包自动更新工具，用于从上游获取最新版本并更新 PKGBUILD 文件。项目使用 Python 3.13+ 开发，采用模块化架构。

## 开发命令

```bash
# 进入项目目录
cd scripts

# 运行程序（使用 uv）
uv run main.py                    # 更新所有包
uv run main.py --all              # 更新所有包（显式）
uv run main.py --package qq       # 更新指定包
uv run main.py --list             # 列出所有可用包

# 运行测试（使用 uv）
uv run pytest                     # 运行所有测试
uv run pytest tests/              # 运行所有测试
uv run pytest tests/fetcher/test_fetcher.py  # 运行单个测试文件

# 依赖管理（使用 uv）
uv sync                           # 同步依赖
uv add <package>                  # 添加新依赖
uv remove <package>               # 移除依赖
```

**重要**: 项目统一使用 `uv` 管理和运行，禁止显式使用 `python` 命令（特殊情况除外）。

## 架构设计

### 核心流程

工具采用三阶段处理流程：**Fetch → Parse → Update**

1. **Fetch** (`fetcher/`): 从网络获取版本信息
2. **Parse** (`parsers/`): 解析数据，提取版本号和下载链接
3. **Update** (`updater/`): 更新 PKGBUILD 文件

### 目录结构

```
scripts/                          # 主要代码目录
├── cli/                          # 命令行接口
│   └── cli.py                    # argparse 入口，处理命令行参数
├── core/
│   └── package_updater.py        # PackageUpdater 类，整合三个阶段流程
├── constants/
│   └── constants.py              # 枚举类：ArchEnum、HashAlgorithmEnum、ParserEnum
├── fetcher/
│   └── fetcher.py                # Fetcher 类，HTTP 客户端封装
├── loaders/
│   └── config_loader.py          # ConfigLoader，加载 packages.yaml 配置
├── parsers/
│   ├── base_parser.py            # BaseParser 抽象基类
│   ├── qq.py                     # QQParser 实现
│   └── navicat.py                # NavicatPremiumCSParser 实现
├── updater/
│   └── pkgbuild_editor.py        # PKGBUILDEditor，编辑 PKGBUILD 文件
├── utils/
│   └── hash.py                   # 哈希计算工具函数
├── tests/                        # pytest 测试目录
├── packages.yaml                 # 包配置文件（核心配置）
└── main.py                       # 程序入口

packages/                         # AUR 包目录
├── linuxqq-nt/                   # QQ Linux 包
│   └── PKGBUILD                  # PKGBUILD 文件
└── navicat17-premium-zh-cn/      # Navicat 包
    └── PKGBUILD                  # PKGBUILD 文件
```

### 关键类和接口

**BaseParser** (`parsers/base_parser.py`)
- 抽象基类，所有解析器必须继承此类
- 实现两个抽象方法：
  - `parse_version(response_data) -> str | None`: 解析版本号
  - `parse_url(arch, response_data) -> str | None`: 解析下载 URL

**PackageUpdater** (`core/package_updater.py`)
- 核心协调器，整合 fetch、parse、update 三个阶段
- `project_root` 指向 `scripts/` 目录
- `pkgbuild_root` 指向项目根目录（用于定位 PKGBUILD 文件）
- 维护 `parsers` 字典，映射 `ParserEnum` 到解析器实例

**PKGBUILDEditor** (`updater/pkgbuild_editor.py`)
- 使用正则表达式编辑 PKGBUILD 文件
- 支持更新 `pkgver`、`pkgrel`、`source_<arch>`、`sha512sums_<arch>` 等字段
- 注意：文件路径处理使用 `Path` 对象，支持相对和绝对路径

### 配置文件结构

**packages.yaml** 示例：
```yaml
packages:
  qq:
    name: qq                                    # 包名
    source: qq                                  # 来源标识
    fetch_url: "https://..."                    # 获取版本信息的 URL
    upstream: "Tencent/QQ"                      # 上游项目
    parser: QQParser                            # 解析器名称（必须匹配 ParserEnum）
    pkgbuild: "packages/linuxqq-nt/PKGBUILD"    # PKGBUILD 相对路径
    update_source_url: true                     # 是否更新 source URL
    arch:                                       # 支持的架构列表
      - x86_64
      - aarch64
      - loong64
```

### 枚举类型

**ArchEnum** (`constants/constants.py`): 支持的架构
- `X86_64`, `AARCH64`, `LOONG64`, `MIPS64EL`

**HashAlgorithmEnum**: 哈希算法
- `SHA256`, `SHA512`

**ParserEnum**: 解析器名称
- 必须与 `PackageUpdater.parsers` 字典的键对应

## 添加新软件包

1. 在 `packages.yaml` 中添加包配置
2. 在 `parsers/` 中创建新的解析器类，继承 `BaseParser`
3. 在 `constants/constants.py` 的 `ParserEnum` 中添加解析器名称
4. 在 `core/package_updater.py` 的 `PackageUpdater.__init__()` 中注册解析器实例
5. 在 `packages/` 目录中创建对应的 PKGBUILD 文件

## 测试

- 使用 `pytest` 和 `pytest-asyncio`
- 测试文件位于 `scripts/tests/` 目录
- 测试使用 `unittest.mock` 进行异步 HTTP 请求模拟

## 注意事项

- **项目使用 uv 统一管理运行环境，禁止显式使用 `python` 命令**
- 项目使用绝对导入（`from cli.cli import update_main`），而不是相对导入
- Python 版本要求 >= 3.13
- PKGBUILD 文件路径相对于项目根目录（`aur-packages/`），而非 `scripts/` 目录
- 下载的文件默认保存在 `scripts/downloads/` 目录
- 支持多架构包，每个架构独立计算校验和

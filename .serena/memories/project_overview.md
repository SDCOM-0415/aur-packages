# 项目概述

## 项目名称
aur-auto-update - Arch Linux AUR 包自动更新工具

## 项目目的
从上游获取最新版本并自动更新 PKGBUILD 文件，支持多架构包管理。

## 技术栈
- **Python**: >= 3.13
- **包管理**: uv (Astral)
- **HTTP 客户端**: httpx[socks] >= 0.28.1
- **配置解析**: pyyaml >= 6.0.3
- **数据验证**: pydantic >= 2.12.5
- **测试框架**: pytest >= 9.0.2, pytest-asyncio >= 1.3.0
- **类型检查**: ty >= 0.0.8 (Astral 快速类型检查器)
- **代码格式**: ruff >= 0.14.10

## 项目架构
三阶段处理流程：**Fetch → Parse → Update**

1. **Fetch** (`fetcher/`): 从网络获取版本信息
2. **Parse** (`parsers/`): 解析数据，提取版本号和下载链接
3. **Update** (`updater/`): 更新 PKGBUILD 文件

## 核心类
- `PackageUpdater`: 核心协调器，整合 fetch、parse、update 三个阶段
- `BaseParser`: 抽象基类，所有解析器必须继承此类，实现 `parse_version()` 和 `parse_url()` 方法
- `PKGBUILDEditor`: 使用正则表达式编辑 PKGBUILD 文件
- `Fetcher`: HTTP 客户端封装

## 目录结构
```
scripts/                          # 主要代码目录
├── cli/                          # 命令行接口
├── core/                         # 核心协调器
├── constants/                    # 枚举类
├── fetcher/                      # HTTP 客户端
├── loaders/                      # 配置加载器
├── parsers/                      # 解析器实现
├── updater/                      # PKGBUILD 编辑器
├── utils/                        # 工具函数
├── tests/                        # pytest 测试
├── packages.yaml                 # 包配置文件
└── main.py                       # 程序入口
```

## 支持的架构
- x86_64
- aarch64
- loong64
- mips64el

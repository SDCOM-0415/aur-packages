# AUR 包自动更新工具

> 🚀 自动化 Arch Linux AUR 包版本更新工具

[![Python](https://img.shields.io/badge/Python-3.13%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ 特性

- 🔄 **自动化更新** - 自动获取最新版本并更新 PKGBUILD
- 🎯 **多架构支持** - x86_64、aarch64、loong64
- 🔐 **自动校验和** - SHA512 校验和计算
- 🧩 **易于扩展** - 插件化解析器设计

## 🚀 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/yourusername/aur-packages.git
cd aur-packages/scripts

# 安装依赖
pip install uv
uv sync
```

### 使用

```bash
# 更新所有包
uv run main.py

# 更新指定包
uv run main.py --package qq

# 列出所有包
uv run main.py --list
```

## 📦 支持的包

- `linuxqq-nt` - QQ Linux
- `navicat17-premium-zh-cn` - Navicat Premium

## 🛠️ 添加新包

1. **编辑配置** (`scripts/packages.yaml`)

```yaml
packages:
  vscode:
    name: vscode
    source: vscode
    source_url: "https://code.visualstudio.com/"
    fetch_url: "https://api.example.com/version"
    upstream: "microsoft/vscode"
    parser: VSCodeParser
    pkgbuild: "packages/vscode/PKGBUILD"
    update_source_url: true
    arch: [x86_64, aarch64]
```

2. **创建解析器** (`scripts/parsers/vscode.py`)

```python
from parsers.base_parser import BaseParser

class VSCodeParser(BaseParser):
    def parse_version(self, response_data):
        return "1.0.0"  # 解析逻辑

    def parse_url(self, arch, response_data):
        return "https://..."  # URL 构造逻辑
```

3. **注册解析器**

在 `constants/constants.py` 和 `core/package_updater.py` 中注册

## 📖 文档

- [快速入门](docs/01-quickstart.md)
- [开发指南](docs/04-development-guide.md)
- [API 参考](docs/03-api-reference.md)
- [常见问题](docs/06-faq.md)

## 🔧 开发

```bash
# 运行测试
uv run pytest

# 同步依赖
uv sync
```

## 📋 技术栈

- Python 3.13+
- httpx (异步 HTTP)
- pydantic (数据验证)
- pytest (测试)
- uv (包管理)

## 📄 许可证

MIT License

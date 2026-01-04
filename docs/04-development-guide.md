# 开发指南

> 🛠️ 详细的开发文档，帮助开发者快速上手和参与项目开发

## 目录

- [开发环境搭建](#开发环境搭建)
- [项目结构详解](#项目结构详解)
- [添加新软件包](#添加新软件包)
- [创建自定义解析器](#创建自定义解析器)
- [测试与调试](#测试与调试)
- [代码规范](#代码规范)
- [开发工作流](#开发工作流)

---

## 开发环境搭建

### 系统要求

- **操作系统**: Linux (推荐 Arch Linux)
- **Python 版本**: >= 3.13
- **包管理器**: `uv` (推荐) 或 `pip`

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/yourusername/aur-packages.git
cd aur-packages
```

#### 2. 安装 uv (推荐)

```bash
# 使用 pip 安装 uv
pip install uv

# 或使用官方安装脚本
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 3. 安装依赖

```bash
# 进入 scripts 目录
cd scripts

# 使用 uv 同步依赖
uv sync
```

#### 4. 验证安装

```bash
# 运行程序
uv run main.py --list

# 运行测试
uv run pytest
```

### 开发工具推荐

- **IDE**: VSCode / PyCharm
- **VSCode 扩展**:
  - Python
  - Pylance
  - YAML
  - Code Runner
- **代码格式化**: `black`
- **代码检查**: `ruff` 或 `flake8`
- **类型检查**: `mypy`

---

## 项目结构详解

### 完整目录树

```
aur-packages/
├── docs/                           # 📚 文档目录
│   ├── README.md                   # 文档索引
│   ├── 01-quickstart.md            # 快速入门
│   ├── 02-architecture.md          # 架构设计
│   ├── 03-api-reference.md         # API 参考
│   ├── 04-development-guide.md     # 开发指南（本文件）
│   ├── 05-configuration.md         # 配置文件说明
│   └── 06-faq.md                   # 常见问题
│
├── scripts/                        # 🔧 主要代码目录
│   ├── __init__.py
│   │
│   ├── cli/                        # 命令行接口
│   │   ├── __init__.py
│   │   └── cli.py                  # argparse 入口
│   │
│   ├── core/                       # 核心逻辑
│   │   ├── __init__.py
│   │   └── package_updater.py      # PackageUpdater 主协调器
│   │
│   ├── constants/                  # 常量定义
│   │   ├── __init__.py
│   │   └── constants.py            # 枚举类定义
│   │
│   ├── fetcher/                    # 数据获取
│   │   ├── __init__.py
│   │   └── fetcher.py              # HTTP 客户端
│   │
│   ├── loaders/                    # 配置加载
│   │   ├── __init__.py
│   │   └── config_loader.py        # YAML 配置加载器
│   │
│   ├── parsers/                    # 版本解析
│   │   ├── __init__.py
│   │   ├── base_parser.py          # 解析器基类
│   │   ├── qq.py                   # QQ 解析器
│   │   └── navicat.py              # Navicat 解析器
│   │
│   ├── updater/                    # PKGBUILD 更新
│   │   ├── __init__.py
│   │   └── pkgbuild_editor.py      # PKGBUILD 文件编辑器
│   │
│   ├── utils/                      # 工具函数
│   │   ├── __init__.py
│   │   └── hash.py                 # 哈希计算工具
│   │
│   ├── tests/                      # 测试代码
│   │   ├── __init__.py
│   │   ├── conftest.py             # pytest 配置
│   │   └── fetcher/
│   │       ├── __init__.py
│   │       └── test_fetcher.py     # Fetcher 测试
│   │
│   ├── downloads/                  # 下载文件缓存（自动创建）
│   ├── packages.yaml               # 包配置文件
│   └── main.py                     # 程序入口
│
├── packages/                       # 📦 AUR 包目录
│   ├── linuxqq-nt/                 # QQ Linux 包
│   │   └── PKGBUILD                # PKGBUILD 文件
│   └── navicat17-premium-zh-cn/    # Navicat 包
│       └── PKGBUILD                # PKGBUILD 文件
│
├── CLAUDE.md                       # Claude Code 项目指引
└── README.md                       # 项目说明
```

### 模块职责说明

#### `cli/` - 命令行接口
- **职责**: 解析命令行参数，调用相应功能
- **核心文件**: `cli.py`
- **依赖**: `core.package_updater`

#### `core/` - 核心逻辑
- **职责**: 整合三个阶段的流程
- **核心文件**: `package_updater.py`
- **依赖**: 所有其他模块

#### `constants/` - 常量定义
- **职责**: 定义枚举类型和常量
- **核心文件**: `constants.py`
- **依赖**: 无

#### `fetcher/` - 数据获取
- **职责**: HTTP 请求封装
- **核心文件**: `fetcher.py`
- **依赖**: `httpx`

#### `loaders/` - 配置加载
- **职责**: 加载和验证 YAML 配置
- **核心文件**: `config_loader.py`
- **依赖**: `pydantic`, `yaml`

#### `parsers/` - 版本解析
- **职责**: 解析各种格式的版本信息
- **核心文件**: `base_parser.py`, `qq.py`, `navicat.py`
- **依赖**: `constants`

#### `updater/` - PKGBUILD 更新
- **职责**: 编辑 PKGBUILD 文件
- **核心文件**: `pkgbuild_editor.py`
- **依赖**: `constants`, `utils.hash`

#### `utils/` - 工具函数
- **职责**: 提供通用工具函数
- **核心文件**: `hash.py`
- **依赖**: 无

---

## 添加新软件包

添加新软件包需要以下步骤：

### 步骤 1: 在 `packages.yaml` 中添加配置

编辑 `scripts/packages.yaml`:

```yaml
packages:
  your-package:
    name: your-package              # 包名
    source: your-source             # 来源标识
    source_url: "https://..."       # 官方网站 URL
    fetch_url: "https://..."        # 获取版本信息的 URL
    upstream: "User/Repo"           # 上游项目
    parser: YourPackageParser       # 解析器名称（待创建）
    pkgbuild: "packages/your-package/PKGBUILD"  # PKGBUILD 路径
    update_source_url: true         # 是否更新 source URL
    arch:
      - x86_64
      - aarch64
      - loong64
```

**配置字段说明**:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | str | ✅ | 包名，通常与 AUR 包名一致 |
| `source` | str | ✅ | 来源标识，用于区分不同来源 |
| `source_url` | str | ✅ | 官方网站 URL |
| `fetch_url` | str | ✅ | 获取版本信息的 API/页面 URL |
| `upstream` | str | ✅ | 上游项目，格式: "Owner/Repo" 或 "Company/Product" |
| `parser` | str | ✅ | 解析器类名，必须添加到 `ParserEnum` |
| `pkgbuild` | str | ✅ | PKGBUILD 文件的相对路径 |
| `update_source_url` | bool | ❌ | 是否更新 source URL，默认 true |
| `arch` | list | ✅ | 支持的架构列表 |

### 步骤 2: 创建解析器

在 `scripts/parsers/` 目录创建新文件 `your_package.py`:

```python
from parsers.base_parser import BaseParser
from constants.constants import ArchEnum
import re
import json

class YourPackageParser(BaseParser):
    """Your Package 解析器"""

    def parse_version(self, response_data):
        """
        从响应数据中提取版本号

        Args:
            response_data: API 响应数据（文本格式）

        Returns:
            版本号字符串或 None
        """
        # 示例 1: 从 HTML 中提取版本号
        match = re.search(r'version["\s:]+(\d+\.\d+\.\d+)', response_data)
        if match:
            return match.group(1)

        # 示例 2: 从 JSON 中提取版本号
        try:
            data = json.loads(response_data)
            return data.get("latest_version")
        except json.JSONDecodeError:
            pass

        return None

    def parse_url(self, arch, response_data):
        """
        从响应数据中提取下载 URL

        Args:
            arch: 目标架构 (ArchEnum)
            response_data: API 响应数据

        Returns:
            下载 URL 或 None
        """
        # 示例 1: 根据版本号构造 URL
        version = self.parse_version(response_data)
        if version:
            base_url = "https://example.com/downloads"
            return f"{base_url}/your-package-{version}-{arch.value}.deb"

        # 示例 2: 从响应数据中提取 URL
        try:
            data = json.loads(response_data)
            downloads = data.get("downloads", {})
            return downloads.get(arch.value)
        except json.JSONDecodeError:
            pass

        return None
```

### 步骤 3: 在 `ParserEnum` 中注册

编辑 `scripts/constants/constants.py`:

```python
class ParserEnum(Enum):
    """解析器枚举"""
    QQ = "QQParser"
    NAVICAT_PREMIUM_CS = "NavicatPremiumCSParser"
    YOUR_PACKAGE = "YourPackageParser"  # 新增
```

### 步骤 4: 在 `PackageUpdater` 中注册解析器

编辑 `scripts/core/package_updater.py`:

```python
from parsers.your_package import YourPackageParser  # 新增导入

class PackageUpdater:
    def __init__(self):
        # ... 其他代码 ...

        self.parsers: dict[str, BaseParser] = {
            ParserEnum.QQ.value: QQParser(),
            ParserEnum.NAVICAT_PREMIUM_CS.value: NavicatPremiumCSParser(),
            ParserEnum.YOUR_PACKAGE.value: YourPackageParser(),  # 新增
        }
```

### 步骤 5: 创建 PKGBUILD 文件

在 `packages/your-package/` 目录创建 `PKGBUILD` 文件:

```bash
# Maintainer: Your Name <your.email@example.com>

pkgname=your-package
pkgver=1.0.0  # 初始版本，程序会自动更新
pkgrel=1
pkgdesc="Your package description"
arch=('x86_64' 'aarch64' 'loong64')
url="https://example.com"
license=('License')
depends=()
options=(!debug)

# 架构特定的源文件和校验和
source_x86_64=("your-package-\${pkgver}-x86_64.deb::https://example.com/downloads/file.deb")
sha512sums_x86_64=('SKIP')

source_aarch64=("your-package-\${pkgver}-aarch64.deb::https://example.com/downloads/file.deb")
sha512sums_aarch64=('SKIP')

source_loong64=("your-package-\${pkgver}-loong64.deb::https://example.com/downloads/file.deb")
sha512sums_loong64=('SKIP')

package() {
    # 安装逻辑
    bsdtar -xf "your-package-\${pkgver}-\${CARCH}.deb"
    cp -r opt/* "${pkgdir}/opt/"
    cp -r usr/* "${pkgdir}/usr/"
}
```

### 步骤 6: 测试

```bash
# 在 scripts 目录下
uv run main.py --package your-package

# 查看输出，确认：
# 1. 能够正确获取版本信息
# 2. 能够正确解析版本号
# 3. 能够正确构造下载 URL
# 4. 能够成功下载文件
# 5. 能够正确更新 PKGBUILD
```

---

## 创建自定义解析器

### 解析器设计原则

1. **单一职责**: 只负责解析，不负责下载和更新
2. **容错处理**: 解析失败返回 `None`，不抛出异常
3. **格式灵活**: 支持多种数据格式（HTML, JSON, XML, JavaScript）
4. **架构支持**: 必须支持多架构

### 解析器模板

```python
from parsers.base_parser import BaseParser
from constants.constants import ArchEnum
from typing import Optional
import re
import json

class CustomParser(BaseParser):
    """自定义解析器模板"""

    def __init__(self):
        """初始化解析器（可选）"""
        super().__init__()
        # 可以添加一些初始化配置
        self.base_url = "https://example.com"

    def parse_version(self, response_data) -> Optional[str]:
        """
        解析版本号

        实现要点：
        1. 处理多种响应格式
        2. 提取版本号
        3. 验证版本号格式
        4. 返回 None 表示解析失败
        """
        if not response_data:
            return None

        # 方法 1: 正则表达式提取
        match = re.search(r'(\d+\.\d+\.\d+)', response_data)
        if match:
            version = match.group(1)
            # 验证版本号格式
            if self._validate_version(version):
                return version

        # 方法 2: JSON 解析
        try:
            data = json.loads(response_data)
            version = data.get("version", data.get("tag_name"))
            if version and self._validate_version(version):
                # 移除 'v' 前缀
                return version.lstrip('v')
        except (json.JSONDecodeError, TypeError):
            pass

        # 方法 3: HTML 解析
        from html.parser import HTMLParser
        # 实现你的 HTML 解析逻辑

        return None

    def parse_url(self, arch: ArchEnum, response_data) -> Optional[str]:
        """
        解析下载 URL

        实现要点：
        1. 支持多架构
        2. 处理相对 URL 和绝对 URL
        3. 构造完整的下载链接
        """
        if not response_data:
            return None

        version = self.parse_version(response_data)
        if not version:
            return None

        # 方法 1: 根据版本号构造 URL
        url = f"{self.base_url}/downloads/v{version}/package-{version}-{arch.value}.deb"
        return url

        # 方法 2: 从响应数据中提取 URL
        # try:
        #     data = json.loads(response_data)
        #     assets = data.get("assets", [])
        #     for asset in assets:
        #         if arch.value in asset["name"]:
        #             return asset["browser_download_url"]
        # except (json.JSONDecodeError, TypeError):
        #     pass

        # return None

    def _validate_version(self, version: str) -> bool:
        """验证版本号格式"""
        pattern = r'^\d+\.\d+\.\d+$'
        return bool(re.match(pattern, version))
```

### 常见解析场景

#### 场景 1: GitHub Release API

```python
def parse_version(self, response_data):
    data = json.loads(response_data)
    tag_name = data.get("tag_name", "")
    # 移除 'v' 前缀
    return tag_name.lstrip('v')

def parse_url(self, arch, response_data):
    data = json.loads(response_data)
    assets = data.get("assets", [])
    for asset in assets:
        name = asset.get("name", "")
        if arch.value in name and name.endswith(".deb"):
            return asset.get("browser_download_url")
    return None
```

#### 场景 2: HTML 页面解析

```python
def parse_version(self, response_data):
    # 提取版本号
    match = re.search(r'<span class="version">(\d+\.\d+\.\d+)</span>', response_data)
    return match.group(1) if match else None

def parse_url(self, arch, response_data):
    version = self.parse_version(response_data)
    base_url = "https://example.com/downloads"
    # 根据架构选择不同的文件名模式
    filename_patterns = {
        ArchEnum.X86_64: f"package-{version}-amd64.deb",
        ArchEnum.AARCH64: f"package-{version}-arm64.deb",
    }
    filename = filename_patterns.get(arch)
    if filename:
        return f"{base_url}/{filename}"
    return None
```

#### 场景 3: JavaScript 配置文件

```python
def parse_version(self, response_data):
    # 从 JavaScript 对象中提取版本号
    match = re.search(r'version\s*[:=]\s*["\'](\d+\.\d+\.\d+)["\']', response_data)
    return match.group(1) if match else None

def parse_url(self, arch, response_data):
    version = self.parse_version(response_data)
    # 从配置中提取下载 URL
    match = re.search(f'downloadUrl_{arch.value}["\s:]+(["\'])([^"\']+)\1', response_data)
    if match:
        return match.group(2)
    return None
```

---

## 测试与调试

### 测试框架

项目使用 `pytest` 和 `pytest-asyncio` 进行测试。

### 测试文件结构

```
scripts/tests/
├── __init__.py
├── conftest.py                 # pytest 配置和 fixtures
├── test_fetcher.py              # Fetcher 测试
├── test_parsers.py              # 解析器测试
└── test_updater.py              # Updater 测试
```

### 编写测试

#### 示例 1: 测试 Fetcher

创建 `scripts/tests/test_fetcher.py`:

```python
import pytest
from unittest.mock import AsyncMock, patch
from fetcher.fetcher import Fetcher

@pytest.mark.asyncio
async def test_fetch_json_success():
    """测试成功获取 JSON 数据"""
    fetcher = Fetcher()

    # Mock HTTP 响应
    with patch.object(fetcher.client, 'get') as mock_get:
        mock_response = AsyncMock()
        mock_response.json.return_value = {"version": "1.0.0"}
        mock_response.raise_for_status = lambda: None
        mock_get.return_value = mock_response

        result = await fetcher.fetch_json("https://api.example.com/version")

        assert result is not None
        assert result["version"] == "1.0.0"
        mock_get.assert_called_once()

@pytest.mark.asyncio
async def test_fetch_json_failure():
    """测试获取 JSON 数据失败"""
    fetcher = Fetcher()

    with patch.object(fetcher.client, 'get') as mock_get:
        mock_get.side_effect = Exception("Network error")

        result = await fetcher.fetch_json("https://api.example.com/version")

        assert result is None
```

#### 示例 2: 测试解析器

创建 `scripts/tests/test_parsers.py`:

```python
import pytest
from parsers.qq import QQParser
from constants.constants import ArchEnum

def test_qq_parser_parse_version():
    """测试 QQ 解析器的版本号提取"""
    parser = QQParser()

    # 模拟响应数据
    mock_data = '''
    {
        "linux": {
            "qq": {
                "version": "3.2.8"
            }
        }
    }
    '''

    version = parser.parse_version(mock_data)

    assert version == "3.2.8"

def test_qq_parser_parse_url():
    """测试 QQ 解析器的 URL 提取"""
    parser = QQParser()

    mock_data = '''
    {
        "linux": {
            "qq": {
                "version": "3.2.8"
            }
        }
    }
    '''

    url = parser.parse_url(ArchEnum.X86_64, mock_data)

    assert url is not None
    assert "3.2.8" in url
    assert "x86_64" in url
    assert url.endswith(".deb")

@pytest.mark.parametrize("arch", [
    ArchEnum.X86_64,
    ArchEnum.AARCH64,
    ArchEnum.LOONG64,
])
def test_qq_parser_all_archs(arch):
    """测试所有架构的 URL 生成"""
    parser = QQParser()
    mock_data = '{"linux":{"qq":{"version":"3.2.8"}}}'

    url = parser.parse_url(arch, mock_data)

    assert url is not None
    assert arch.value in url
```

#### 示例 3: 测试 PKGBUILDEditor

创建 `scripts/tests/test_updater.py`:

```python
import pytest
from pathlib import Path
from updater.pkgbuild_editor import PKGBUILDEditor

@pytest.fixture
def temp_pkgbuild(tmp_path):
    """创建临时 PKGBUILD 文件"""
    pkgbuild_content = """pkgname=test-package
pkgver=1.0.0
pkgrel=1
arch=('x86_64')
source_x86_64=('https://example.com/file.deb')
sha512sums_x86_64=('abc123...')
"""
    pkgbuild_path = tmp_path / "PKGBUILD"
    pkgbuild_path.write_text(pkgbuild_content)
    return pkgbuild_path

def test_update_pkgver(temp_pkgbuild):
    """测试更新版本号"""
    editor = PKGBUILDEditor(temp_pkgbuild)

    editor.update_pkgver("2.0.0")
    editor.save()

    # 重新加载验证
    editor.reload()
    assert editor.get_pkgver() == "2.0.0"

def test_update_pkgrel(temp_pkgbuild):
    """测试更新发布号"""
    editor = PKGBUILDEditor(temp_pkgbuild)

    editor.update_pkgrel(2)
    editor.save()

    editor.reload()
    assert editor.get_pkgrel() == 2
```

### 运行测试

```bash
# 运行所有测试
uv run pytest

# 运行单个测试文件
uv run pytest tests/test_fetcher.py

# 运行单个测试函数
uv run pytest tests/test_parsers.py::test_qq_parser_parse_version

# 显示详细输出
uv run pytest -v

# 显示打印输出
uv run pytest -s

# 生成覆盖率报告
uv run pytest --cov=. --cov-report=html
```

### 调试技巧

#### 1. 使用 print 调试

```python
def parse_version(self, response_data):
    print(f"响应数据: {response_data[:200]}...")  # 打印前 200 个字符
    # ... 解析逻辑
```

#### 2. 使用 logging 模块

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def parse_version(self, response_data):
    logger.debug(f"解析版本号，数据长度: {len(response_data)}")
    # ... 解析逻辑
```

#### 3. 使用 pdb 调试器

```python
import pdb

def parse_version(self, response_data):
    pdb.set_trace()  # 设置断点
    # ... 解析逻辑
```

#### 4. 使用 IDE 调试器

- VSCode: 设置断点，按 F5 启动调试
- PyCharm: 点击行号设置断点，点击调试按钮

---

## 代码规范

### Python 代码规范

项目遵循 [PEP 8](https://pep8.org/) 代码风格指南。

#### 命名规范

- **类名**: 大驼峰命名法（PascalCase）
  ```python
  class PackageUpdater:
      pass
  ```

- **函数和变量**: 小写加下划线（snake_case）
  ```python
  def update_package(package_name):
      max_version = 1
  ```

- **常量**: 全大写加下划线
  ```python
  DOWNLOAD_DIR = "downloads"
  DEFAULT_TIMEOUT = 10
  ```

- **私有方法**: 单下划线前缀
  ```python
  def _internal_method(self):
      pass
  ```

#### 类型注解

所有公共方法必须添加类型注解：

```python
from typing import Optional, List, Dict

def parse_version(
    self,
    response_data: str | Any
) -> Optional[str]:
    """解析版本号"""
    pass

def get_supported_archs(self) -> List[ArchEnum]:
    """获取支持的架构"""
    pass
```

#### 文档字符串

使用 Google 风格的文档字符串：

```python
def update_package(
    self,
    package_name: str,
    package_config: PackageConfig
) -> bool:
    """
    更新单个包

    Args:
        package_name: 包名
        package_config: 包配置对象

    Returns:
        更新是否成功

    Example:
        >>> updater = PackageUpdater()
        >>> success = await updater.update_package("qq", config)
    """
    pass
```

#### 导入顺序

1. 标准库导入
2. 第三方库导入
3. 本地模块导入

每组之间用空行分隔：

```python
import re
from pathlib import Path
from typing import Optional

import httpx
from pydantic import BaseModel

from constants.constants import ArchEnum, ParserEnum
from parsers.base_parser import BaseParser
```

### Git 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<类型>(<范围>): <描述>

[可选的正文]

[可选的脚注]
```

#### 类型

- `feat`: 新功能
- `fix`: 修复 bug
- `refactor`: 重构代码
- `docs`: 文档更新
- `test`: 测试相关
- `chore`: 构建/工具链相关

#### 示例

```bash
feat(parser): 添加 VSCode 包解析器

- 新增 VSCodeParser 类
- 支持 x86_64 和 aarch64 架构
- 从官方 API 获取版本信息

Closes #123
```

```bash
fix(core): 修复 PKGBUILD 路径错误

修复 _get_pkgbuild_path 方法中路径拼接错误，
现在能正确处理相对路径和绝对路径。

Fixes #456
```

---

## 开发工作流

### 功能开发流程

1. **创建功能分支**
   ```bash
   git checkout -b feat/add-vscode-package
   ```

2. **编写代码**
   - 添加新功能
   - 编写测试
   - 更新文档

3. **本地测试**
   ```bash
   # 运行测试
   uv run pytest

   # 运行程序
   uv run main.py --list
   ```

4. **提交代码**
   ```bash
   git add .
   git commit -m "feat(parser): 添加 VSCode 包解析器"
   ```

5. **推送到远程**
   ```bash
   git push origin feat/add-vscode-package
   ```

6. **创建 Pull Request**
   - 在 GitHub 上创建 PR
   - 填写 PR 描述
   - 等待代码审查

### Bug 修复流程

1. **创建问题分支**
   ```bash
   git checkout -b fix/pkgbuild-path-error
   ```

2. **定位问题**
   - 阅读错误日志
   - 添加调试输出
   - 运行测试

3. **修复问题**
   - 修改代码
   - 添加回归测试

4. **验证修复**
   ```bash
   uv run pytest tests/test_updater.py -v
   ```

5. **提交并推送**
   ```bash
   git add .
   git commit -m "fix(core): 修复 PKGBUILD 路径错误"
   git push origin fix/pkgbuild-path-error
   ```

### 代码审查清单

在提交 PR 前，请确认：

- [ ] 代码符合 PEP 8 规范
- [ ] 所有测试通过
- [ ] 添加了必要的文档
- [ ] 更新了相关配置文件
- [ ] 提交信息符合规范
- [ ] 没有引入新的警告
- [ ] 代码已自审和简化

---

**最后更新**: 2026-01-04

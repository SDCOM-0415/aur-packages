# 配置文件说明

> ⚙️ 详细的配置文件文档，包含所有配置选项和示例

## 目录

- [配置文件概述](#配置文件概述)
- [全局配置](#全局配置)
- [包配置](#包配置)
- [配置示例](#配置示例)
- [高级配置](#高级配置)
- [配置验证](#配置验证)

---

## 配置文件概述

### 文件位置

```
aur-packages/scripts/packages.yaml
```

### 配置格式

YAML 格式，使用 `pydantic` 进行数据验证。

### 配置结构

```yaml
packages:
  <包名>:
    # 包配置项
```

---

## 全局配置

目前项目没有全局配置项，所有配置都在包级别。

---

## 包配置

### 配置字段

| 字段名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `name` | str | ✅ | - | 包名（标识符） |
| `source` | str | ✅ | - | 来源标识 |
| `source_url` | str | ✅ | - | 官方网站 URL |
| `fetch_url` | str | ✅ | - | 获取版本信息的 API/页面 URL |
| `upstream` | str | ✅ | - | 上游项目（格式: "Owner/Repo" 或 "Company/Product"） |
| `parser` | str | ✅ | - | 解析器名称（必须匹配 ParserEnum） |
| `pkgbuild` | str | ✅ | - | PKGBUILD 文件相对路径 |
| `update_source_url` | bool | ❌ | `true` | 是否更新 PKGBUILD 中的 source URL |
| `arch` | list | ✅ | - | 支持的架构列表 |

### 字段详细说明

#### `name`

**类型**: `str`
**必填**: ✅
**示例**: `"qq"`, `"navicat-premium-zh-cn"`

**说明**:
- 包的唯一标识符
- 用于命令行参数: `--package <name>`
- 建议使用小写字母和连字符

**示例**:
```yaml
name: linuxqq-nt
```

#### `source`

**类型**: `str`
**必填**: ✅
**示例**: `"qq"`, `"navicat-premium-cs"`

**说明**:
- 来源标识，用于区分不同来源
- 可用于日志记录和调试
- 一般与包名相似但不完全相同

**示例**:
```yaml
source: qq
source: navicat-premium-cs
```

#### `source_url`

**类型**: `str` (URL)
**必填**: ✅
**示例**: `"https://im.qq.com/linuxqq/index.shtml"`

**说明**:
- 软件包的官方网站
- 用于文档和参考
- 用户可以通过此链接访问原始发布页面

**示例**:
```yaml
source_url: "https://im.qq.com/linuxqq/index.shtml"
source_url: "https://www.navicat.com.cn/products/navicat-premium"
```

#### `fetch_url`

**类型**: `str` (URL)
**必填**: ✅
**示例**: `"https://api.github.com/repos/user/repo/releases/latest"`

**说明**:
- 获取版本信息的 API 端点或页面 URL
- 由 `Fetcher` 请求
- 返回的数据由 `Parser` 解析

**数据格式支持**:
- JSON API
- HTML 页面
- JavaScript 配置文件
- 纯文本

**示例**:
```yaml
# GitHub API
fetch_url: "https://api.github.com/repos/Tencent/QQ/releases/latest"

# HTML 页面
fetch_url: "https://www.example.com/downloads"

# JavaScript 配置
fetch_url: "https://cdn.example.com/config.js"
```

#### `upstream`

**类型**: `str`
**必填**: ✅
**示例**: `"Tencent/QQ"`, `"PremiumSoft CyberTech Ltd./Navicat Premium"`

**说明**:
- 上游项目信息
- 格式: `"Owner/Repo"` 或 `"Company/Product"`
- 用于文档和追踪

**示例**:
```yaml
upstream: "Tencent/QQ"
upstream: "microsoft/vscode"
upstream: "PremiumSoft CyberTech Ltd./Navicat Premium"
```

#### `parser`

**类型**: `str`
**必填**: ✅
**示例**: `"QQParser"`, `"NavicatPremiumCSParser"`

**说明**:
- 解析器类名
- 必须在 `ParserEnum` 中定义
- 对应的类必须继承 `BaseParser`

**如何添加新解析器**:
1. 在 `scripts/constants/constants.py` 的 `ParserEnum` 中添加
2. 在 `scripts/core/package_updater.py` 中注册实例

**示例**:
```yaml
parser: QQParser
parser: NavicatPremiumCSParser
parser: VSCodeParser
```

#### `pkgbuild`

**类型**: `str` (路径)
**必填**: ✅
**示例**: `"packages/linuxqq-nt/PKGBUILD"`

**说明**:
- PKGBUILD 文件的路径
- 支持相对路径和绝对路径
- 相对路径相对于项目根目录（`aur-packages/`）

**路径规则**:
```yaml
# 相对路径（推荐）
pkgbuild: "packages/linuxqq-nt/PKGBUILD"

# 绝对路径
pkgbuild: "/home/user/aur-packages/packages/linuxqq-nt/PKGBUILD"
```

**注意**:
- 使用正斜杠 `/`（即使在 Windows 上）
- 确保路径存在且可访问
- 建议使用相对路径便于项目迁移

#### `update_source_url`

**类型**: `bool`
**必填**: ❌
**默认值**: `true`
**示例**: `true`, `false`

**说明**:
- 是否在更新时修改 `source_<arch>` 字段
- `true`: 自动更新下载 URL
- `false`: 保持 PKGBUILD 中的 URL 不变

**使用场景**:

**设置为 `true`**:
- 下载 URL 随版本变化
- URL 包含版本号

**设置为 `false`**:
- 下载 URL 固定不变
- PKGBUILD 中已经配置了正确的 URL

**示例**:
```yaml
# URL 随版本变化
update_source_url: true
# PKGBUILD 中的 URL 会从:
# source_x86_64=('https://example.com/app-1.0.0-x86_64.deb')
# 更新为:
# source_x86_64=('https://example.com/app-1.1.0-x86_64.deb')

# URL 固定
update_source_url: false
# PKGBUILD 中的 URL 保持不变
```

#### `arch`

**类型**: `list[str]`
**必填**: ✅
**示例**: `["x86_64", "aarch64", "loong64"]`

**说明**:
- 支持的 CPU 架构列表
- 每个架构必须对应 PKGBUILD 中的配置
- 架构名必须在 `ArchEnum` 中定义

**支持的架构**:
- `x86_64`: AMD64/Intel 64 位
- `aarch64`: ARM 64 位
- `loong64`: 龙芯 64 位
- `mips64el`: MIPS 64 位 Little Endian

**示例**:
```yaml
# 支持所有常见架构
arch:
  - x86_64
  - aarch64
  - loong64

# 仅支持 x86_64
arch:
  - x86_64

# 支持 ARM 和 x86
arch:
  - x86_64
  - aarch64
```

---

## 配置示例

### 示例 1: QQ Linux 包

```yaml
qq:
  name: qq
  source: qq
  source_url: "https://im.qq.com/linuxqq/index.shtml"
  fetch_url: "https://cdn-go.cn/qq-web/im.qq.com_new/latest/rainbow/linuxConfig.js"
  upstream: "Tencent/QQ"
  parser: QQParser
  pkgbuild: "packages/linuxqq-nt/PKGBUILD"
  update_source_url: true
  arch:
    - x86_64
    - aarch64
    - loong64
```

**特点**:
- JavaScript 配置文件作为数据源
- 支持 3 个架构
- URL 随版本变化

### 示例 2: Navicat Premium

```yaml
navicat:
  name: navicat-premium-zh-cn
  source: navicat-premium-cs
  source_url: "https://www.navicat.com.cn/products/navicat-premium"
  fetch_url: "https://www.navicat.com.cn/products/navicat-premium-release-note#L"
  upstream: "PremiumSoft CyberTech Ltd./Navicat Premium"
  parser: NavicatPremiumCSParser
  pkgbuild: "packages/navicat17-premium-zh-cn/PKGBUILD"
  update_source_url: false
  arch:
    - x86_64
    - aarch64
```

**特点**:
- HTML 发布说明作为数据源
- 固定下载 URL（AppImage 格式）
- 仅支持 2 个架构

### 示例 3: GitHub Release 包

```yaml
vscode:
  name: vscode
  source: vscode
  source_url: "https://code.visualstudio.com/"
  fetch_url: "https://api.github.com/repos/microsoft/vscode/releases/latest"
  upstream: "microsoft/vscode"
  parser: GitHubReleaseParser
  pkgbuild: "packages/vscode/PKGBUILD"
  update_source_url: true
  arch:
    - x86_64
    - aarch64
```

**特点**:
- GitHub Release API 作为数据源
- 标准的 JSON API
- 需要创建 `GitHubReleaseParser`

### 示例 4: HTML 解析包

```yaml
sublime-text:
  name: sublime-text
  source: sublime-text
  source_url: "https://www.sublimetext.com/"
  fetch_url: "https://www.sublimetext.com/download"
  upstream: "Sublime HQ Pty Ltd./Sublime Text"
  parser: SublimeTextParser
  pkgbuild: "packages/sublime-text/PKGBUILD"
  update_source_url: true
  arch:
    - x86_64
    - aarch64
```

**特点**:
- HTML 页面作为数据源
- 需要解析 HTML 提取版本号
- 解析器需要处理 HTML 格式

---

## 高级配置

### 条件配置

虽然 YAML 不支持条件语句，但你可以通过多个包配置实现类似效果：

```yaml
qq-stable:
  name: qq
  source: qq
  fetch_url: "https://example.com/qq/stable"
  parser: QQParser
  pkgbuild: "packages/qq-stable/PKGBUILD"
  arch: [x86_64, aarch64]

qq-beta:
  name: qq-beta
  source: qq
  fetch_url: "https://example.com/qq/beta"
  parser: QQParser
  pkgbuild: "packages/qq-beta/PKGBUILD"
  arch: [x86_64, aarch64]
```

### 环境变量

配置文件不支持直接引用环境变量，但可以在代码中处理：

```python
import os
from loaders.config_loader import ConfigLoader

# 加载配置
loader = ConfigLoader.load_from_yaml()

# 根据环境变量选择不同的配置
env = os.getenv("ENV", "production")
package = loader.packages[f"qq-{env}"]
```

### 配置继承

YAML 不支持继承，但可以使用锚点和别名：

```yaml
# 定义通用配置
_x86_64_only: &x86_64_only
  arch:
    - x86_64

# 使用别名
qq:
  name: qq
  source: qq
  # ...
  <<: *x86_64_only

vscode:
  name: vscode
  source: vscode
  # ...
  <<: *x86_64_only
```

---

## 配置验证

### 自动验证

配置文件在加载时自动验证（使用 `pydantic`）：

```python
from loaders.config_loader import ConfigLoader

try:
    loader = ConfigLoader.load_from_yaml("packages.yaml")
except ValidationError as e:
    print(f"配置错误: {e}")
except FileNotFoundError:
    print("配置文件不存在")
except yaml.YAMLError:
    print("YAML 格式错误")
```

### 常见验证错误

#### 1. 缺少必填字段

```yaml
# 错误：缺少 name 字段
qq:
  source: qq
  fetch_url: "https://..."
```

**错误信息**:
```
ValidationError: 1 validation error for PackageConfig
name
  field required (type=value_error.missing)
```

#### 2. 类型错误

```yaml
# 错误：arch 应该是列表
qq:
  name: qq
  arch: x86_64  # 应该是 ["x86_64"]
```

**错误信息**:
```
ValidationError: 1 validation error for PackageConfig
arch
  none is not an allowed value (type=type_error.none.not_allowed)
```

#### 3. 枚举值错误

```yaml
# 错误：架构名称无效
qq:
  name: qq
  arch:
    - amd64  # 应该是 x86_64
```

**处理**: 代码中会跳过无效的架构

### 手动验证

在添加新配置后，建议手动验证：

```bash
# 1. 检查 YAML 语法
uv run python -c "import yaml; yaml.safe_load(open('scripts/packages.yaml'))"

# 2. 测试配置加载
cd scripts
uv run python -c "from loaders.config_loader import ConfigLoader; ConfigLoader.load_from_yaml()"

# 3. 列出所有包
uv run main.py --list
```

---

## 配置最佳实践

### 1. 命名规范

```yaml
# ✅ 好的命名
name: linuxqq-nt
name: navicat-premium-zh-cn

# ❌ 避免
name: LinuxQQ_NT
name: navicat_premium
```

### 2. URL 管理

```yaml
# ✅ 使用引号包裹 URL
source_url: "https://example.com/"
fetch_url: "https://api.example.com/v1"

# ❌ 避免（可能解析错误）
source_url: https://example.com/
```

### 3. 架构顺序

```yaml
# ✅ 按字母顺序排列
arch:
  - aarch64
  - loong64
  - x86_64

# ❌ 避免随机顺序
arch:
  - x86_64
  - aarch64
  - loong64
```

### 4. 注释说明

```yaml
# 腾讯 QQ Linux 版本
# 数据源：JavaScript 配置文件
# 最后验证：2026-01-04
qq:
  name: qq
  source: qq
  fetch_url: "https://cdn-go.cn/qq-web/im.qq.com_new/latest/rainbow/linuxConfig.js"
  # ...
```

### 5. 分组管理

对于大量包，可以按类别分组：

```yaml
packages:
  # 即时通讯
  qq:
    name: qq
    # ...
  wechat:
    name: wechat
    # ...

  # 开发工具
  vscode:
    name: vscode
    # ...
  sublime-text:
    name: sublime-text
    # ...

  # 数据库工具
  navicat:
    name: navicat
    # ...
  dbeaver:
    name: dbeaver
    # ...
```

---

## 配置调试

### 查看配置

```python
from loaders.config_loader import ConfigLoader

loader = ConfigLoader.load_from_yaml()

# 列出所有包
for name, config in loader.packages.items():
    print(f"包名: {name}")
    print(f"  解析器: {config.parser}")
    print(f"  架构: {config.arch}")
    print(f"  PKGBUILD: {config.pkgbuild}")
    print()
```

### 测试单个包

```bash
# 测试特定包的更新流程
python main.py --package qq
```

### 验证路径

```python
from pathlib import Path
from loaders.config_loader import ConfigLoader

loader = ConfigLoader.load_from_yaml()

# 检查 PKGBUILD 文件是否存在
for name, config in loader.packages.items():
    pkgbuild_path = Path(config.pkgbuild)
    if pkgbuild_path.exists():
        print(f"✓ {name}: PKGBUILD 存在")
    else:
        print(f"✗ {name}: PKGBUILD 不存在 ({pkgbuild_path})")
```

---

## 配置迁移

### 从旧版本迁移

如果配置文件格式发生变化，可以创建迁移脚本：

```python
import yaml

def migrate_config(old_file, new_file):
    """迁移旧配置到新格式"""
    with open(old_file) as f:
        old_data = yaml.safe_load(f)

    new_data = {"packages": {}}

    for name, config in old_data.get("packages", {}).items():
        # 转换配置格式
        new_data["packages"][name] = {
            "name": name,
            "source": config.get("source", name),
            "fetch_url": config["url"],
            # ... 其他字段
        }

    with open(new_file, "w") as f:
        yaml.dump(new_data, f, default_flow_style=False)

# 使用
migrate_config("packages.yaml.old", "packages.yaml")
```

---

**最后更新**: 2026-01-04

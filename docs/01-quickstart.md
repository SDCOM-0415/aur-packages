# 快速入门

> 🚀 快速开始使用 AUR 包自动更新工具

## 目录

- [项目简介](#项目简介)
- [环境要求](#环境要求)
- [安装配置](#安装配置)
- [基本使用](#基本使用)
- [常见使用场景](#常见使用场景)
- [下一步](#下一步)

---

## 项目简介

AUR 包自动更新工具是一个用于从上游获取最新版本并自动更新 PKGBUILD 文件的 Python 工具。它支持多架构包，可以自动下载文件、计算校验和，并更新 PKGBUILD 文件。

### 核心特性

- ✅ **自动化**: 自动检测新版本并更新 PKGBUILD
- 🎯 **多架构支持**: 支持 x86_64、aarch64、loong64 等架构
- 🔐 **校验和验证**: 自动计算 SHA512 校验和
- 🧩 **可扩展**: 易于添加新软件包和解析器
- ⚡ **异步处理**: 使用 httpx 进行高效的异步网络请求

### 支持的软件包

目前支持以下软件包：

- **QQ Linux** (`linuxqq-nt`): 腾讯 QQ Linux 版本
- **Navicat Premium** (`navicat17-premium-zh-cn`): Navicat Premium 数据库管理工具

---

## 环境要求

### 系统要求

- **操作系统**: Linux (推荐 Arch Linux)
- **Python 版本**: >= 3.13

### Python 依赖

- `httpx`: 异步 HTTP 客户端
- `pydantic`: 数据验证
- `pyyaml`: YAML 配置解析

### 可选依赖

- `pytest`: 测试框架
- `pytest-asyncio`: 异步测试支持

**重要**: 项目统一使用 `uv` 管理和运行，禁止显式使用 `python` 命令。

---

## 安装配置

### 方法 1: 使用 uv (推荐)

#### 1. 安装 uv

```bash
pip install uv
```

#### 2. 克隆项目

```bash
git clone https://github.com/yourusername/aur-packages.git
cd aur-packages
```

#### 3. 安装依赖

```bash
cd scripts
uv sync
```

### 方法 2: 使用 pip

#### 1. 克隆项目

```bash
git clone https://github.com/yourusername/aur-packages.git
cd aur-packages/scripts
```

#### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows
```

#### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 验证安装

```bash
# 确保在 scripts 目录下
uv run main.py --list
```

如果看到以下输出，说明安装成功：

```
可用的包:
  - qq
  - navicat
```

---

## 基本使用

### 命令行语法

```bash
uv run main.py [选项]
```

### 可用选项

| 选项 | 说明 | 示例 |
|------|------|------|
| 无选项 | 更新所有包 | `uv run main.py` |
| `--all` | 更新所有包（显式） | `uv run main.py --all` |
| `--package <包名>` | 更新指定包 | `uv run main.py --package qq` |
| `--list` | 列出所有可用包 | `uv run main.py --list` |

### 更新所有包

```bash
cd scripts
uv run main.py
```

**输出示例**:

```
开始更新所有包...

开始更新包: qq
  1. 从 https://cdn-go.cn/qq-web/im.qq.com_new/latest/rainbow/linuxConfig.js 获取版本信息...
  2. 解析版本信息...
  最新版本: 3.2.8
  PKGBUILD路径: /home/user/aur-packages/packages/linuxqq-nt/PKGBUILD
  当前版本: 3.2.7
  3. 下载文件并计算校验和...
  支持的架构: ['x86_64', 'aarch64', 'loong64']
    下载 x86_64 架构文件: https://dldir1.qq.com/...
    x86_64 架构校验和: abc123...
    下载 aarch64 架构文件: https://dldir1.qq.com/...
    aarch64 架构校验和: def456...
    下载 loong64 架构文件: https://dldir1.qq.com/...
    loong64 架构校验和: ghi789...
  4. 更新PKGBUILD...
  5. PKGBUILD已更新
包 qq 更新完成!

开始更新包: navicat
  ...

更新完成: 2/2 个包更新成功
```

### 更新单个包

```bash
uv run main.py --package qq
```

**输出示例**:

```
开始更新包: qq
  1. 从 https://cdn-go.cn/qq-web/im.qq.com_new/latest/rainbow/linuxConfig.js 获取版本信息...
  2. 解析版本信息...
  最新版本: 3.2.8
  PKGBUILD路径: /home/user/aur-packages/packages/linuxqq-nt/PKGBUILD
  当前版本: 3.2.8
  版本已是最新，无需更新
```

### 列出所有可用包

```bash
uv run main.py --list
```

**输出示例**:

```
可用的包:
  - qq
  - navicat
```

---

## 常见使用场景

### 场景 1: 日常更新 AUR 包

作为 AUR 包维护者，你需要定期检查并更新包的版本。

**步骤**:

1. **运行更新工具**
   ```bash
   cd ~/aur-packages/scripts
   uv run main.py
   ```

2. **检查输出**
   - 工具会自动检测新版本
   - 如果版本已是最新，会跳过更新

3. **验证 PKGBUILD**
   ```bash
   cd ../packages/linuxqq-nt
   cat PKGBUILD | grep pkgver
   ```

4. **测试构建**
   ```bash
   makepkg -si
   ```

5. **提交到 AUR**
   ```bash
   git add PKGBUILD
   git commit -m "upgpkg: update to 3.2.8"
   git push
   ```

### 场景 2: 添加新软件包

你想为一个新的软件包添加自动更新功能。

**步骤**:

1. **准备 PKGBUILD**
   - 在 `packages/` 目录创建包目录
   - 编写或复制 PKGBUILD 文件

2. **编辑配置文件**
   ```bash
   cd scripts
   vim packages.yaml
   ```

   添加新包配置：
   ```yaml
   packages:
     vscode:
       name: vscode
       source: vscode
       source_url: "https://code.visualstudio.com/"
       fetch_url: "https://update.code.visualstudio.com/api/update/linux-x64/stable/VERSION"
       upstream: "microsoft/vscode"
       parser: VSCodeParser
       pkgbuild: "packages/vscode/PKGBUILD"
       update_source_url: true
       arch:
         - x86_64
         - aarch64
   ```

3. **创建解析器**
   ```bash
   vim parsers/vscode.py
   ```

   实现 `BaseParser` 接口。

4. **注册解析器**
   - 在 `constants/constants.py` 的 `ParserEnum` 中添加
   - 在 `core/package_updater.py` 中注册

5. **测试**
   ```bash
   uv run main.py --package vscode
   ```

详细步骤请参考 [开发指南](./04-development-guide.md)。

### 场景 3: 调试解析器

你发现某个包的版本号解析不正确。

**步骤**:

1. **手动检查数据源**
   ```bash
   curl -s https://example.com/api/version
   ```

2. **测试解析器**
   ```python
   from parsers.qq import QQParser
   import httpx

   async def test():
       parser = QQParser()
       async with httpx.AsyncClient() as client:
           response = await client.get("https://example.com/api/version")
           data = response.text
           version = parser.parse_version(data)
           print(f"版本: {version}")

   import asyncio
   asyncio.run(test())
   ```

3. **修复解析器**
   - 根据实际数据格式调整正则表达式或 JSON 解析逻辑
   - 保存文件

4. **重新测试**
   ```bash
   python main.py --package qq
   ```

### 场景 4: 批量更新多个包

你有多个 AUR 包需要更新。

**步骤**:

1. **一次性更新所有包**
   ```bash
   python main.py
   ```

2. **查看更新摘要**
   ```
   更新完成: 5/7 个包更新成功
   ```

3. **处理失败的包**
   - 查看错误信息
   - 手动检查数据源
   - 修复解析器或配置

---

## 核心概念

### 三阶段流程

工具采用三阶段处理流程：

```
┌─────────┐      ┌─────────┐      ┌─────────┐
│  Fetch  │  →   │  Parse  │  →   │  Update │
└─────────┘      └─────────┘      └─────────┘
   获取数据         解析信息        更新文件
```

#### Fetch 阶段
- 使用 `Fetcher` 类从网络获取数据
- 支持 JSON 和文本格式
- 异步 HTTP 请求

#### Parse 阶段
- 使用特定解析器解析数据
- 提取版本号和下载 URL
- 支持多架构

#### Update 阶段
- 下载各架构的文件
- 计算校验和（SHA512）
- 更新 PKGBUILD 文件

### 目录结构

```
aur-packages/
├── scripts/              # 主程序目录
│   ├── cli/             # 命令行接口
│   ├── core/            # 核心逻辑
│   ├── parsers/         # 解析器
│   ├── updater/         # PKGBUILD 编辑器
│   ├── fetcher/         # HTTP 客户端
│   ├── loaders/         # 配置加载器
│   ├── utils/           # 工具函数
│   └── packages.yaml    # 配置文件
│
└── packages/            # AUR 包目录
    ├── linuxqq-nt/
    │   └── PKGBUILD
    └── navicat17-premium-zh-cn/
        └── PKGBUILD
```

### 配置文件

`packages.yaml` 是核心配置文件，定义了所有包的信息：

```yaml
packages:
  qq:
    name: qq                              # 包名
    source: qq                            # 来源
    fetch_url: "https://..."               # 数据源 URL
    upstream: "Tencent/QQ"                # 上游项目
    parser: QQParser                      # 解析器
    pkgbuild: "packages/linuxqq-nt/PKGBUILD"  # PKGBUILD 路径
    update_source_url: true               # 是否更新 URL
    arch:                                 # 支持的架构
      - x86_64
      - aarch64
      - loong64
```

---

## 常见问题

### Q1: 如何查看程序执行详情？

**A**: 程序默认输出详细的执行过程，包括：
- 获取版本信息的 URL
- 解析的版本号
- 下载进度
- 计算的校验和

如果需要更详细的调试信息，可以修改代码添加 `print` 语句或使用 `logging` 模块。

### Q2: 下载的文件保存在哪里？

**A**: 下载的文件默认保存在 `scripts/downloads/` 目录。

文件命名格式：`{package_name}_{version}_{arch}.deb`

例如：`qq_3.2.8_x86_64.deb`

### Q3: 如何只检查版本但不更新？

**A**: 目前工具没有提供"仅检查"选项。你可以：
1. 临时注释掉 `update_package()` 中的更新代码
2. 或者创建一个自定义的检查脚本

示例：

```python
async def check_only():
    updater = PackageUpdater()
    for name, config in updater.config.packages.items():
        response = await updater.fetcher.fetch_text(config.fetch_url)
        parser = updater.parsers[config.parser]
        version = parser.parse_version(response)
        print(f"{name}: {version}")
```

### Q4: 支持哪些架构？

**A**: 支持以下架构：
- x86_64 (AMD64/Intel 64)
- aarch64 (ARM 64)
- loong64 (龙芯 64)
- mips64el (MIPS 64 Little Endian)

### Q5: 如何处理网络错误？

**A**: 工具内置了错误处理：
- 网络请求失败会打印错误信息
- 解析失败会返回 `None`
- 下载失败会跳过当前包

如果网络不稳定，可以：
1. 增加超时时间（修改 `Fetcher.__init__` 的 `timeout` 参数）
2. 使用代理（设置环境变量 `HTTP_PROXY` 和 `HTTPS_PROXY`）
3. 重试失败的包

### Q6: PKGBUILD 路径如何指定？

**A**: `pkgbuild` 字段支持相对路径和绝对路径：

- **相对路径**: 相对于项目根目录（`aur-packages/`）
  ```yaml
  pkgbuild: "packages/linuxqq-nt/PKGBUILD"
  ```

- **绝对路径**: 完整的系统路径
  ```yaml
  pkgbuild: "/home/user/aur-packages/packages/linuxqq-nt/PKGBUILD"
  ```

推荐使用相对路径，便于项目迁移。

---

## 下一步

恭喜！你已经掌握了基本使用方法。

### 推荐阅读

1. **[架构设计](./02-architecture.md)** - 深入了解项目架构
2. **[API 参考](./03-api-reference.md)** - 查看完整的 API 文档
3. **[开发指南](./04-development-guide.md)** - 学习如何添加新包和创建解析器
4. **[配置文件说明](./05-configuration.md)** - 详细的配置选项

### 实践建议

1. **先测试再提交**: 在本地测试 PKGBUILD 构建
2. **版本检查**: 确认新版本在上游确实可用
3. **备份配置**: 在修改配置文件前做好备份
4. **查看日志**: 遇到问题时仔细阅读错误信息

### 获取帮助

- **GitHub Issues**: 报告 bug 或请求功能
- **文档**: 查看完整文档
- **源代码**: 阅读源代码了解实现细节

---

**最后更新**: 2026-01-04

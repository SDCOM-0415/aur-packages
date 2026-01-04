# 架构设计

> 🏗️ 项目架构设计文档，详细说明系统的设计原则、模块划分和交互流程

## 目录

- [架构概览](#架构概览)
- [核心流程](#核心流程)
- [模块设计](#模块设计)
- [数据流](#数据流)
- [设计模式](#设计模式)
- [技术栈](#技术栈)
- [架构决策](#架构决策)

---

## 架构概览

### 设计理念

AUR 包自动更新工具采用**模块化、可扩展**的架构设计，核心思想是：

1. **关注点分离**: 将获取、解析、更新三个阶段解耦
2. **开闭原则**: 对扩展开放，对修改关闭
3. **依赖注入**: 通过配置文件注入解析器
4. **异步优先**: 使用异步 I/O 提高性能

### 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                         用户接口层                            │
│                    (CLI: main.py, cli.py)                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        核心协调层                             │
│                   (PackageUpdater)                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │  Fetch   │→ │  Parse   │→ │  Update  │                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
└─────────────────────────────────────────────────────────────┘
       │                │                │
       ▼                ▼                ▼
┌──────────┐    ┌──────────┐    ┌──────────┐
│ Fetcher  │    │ Parsers  │    │ Updater  │
└──────────┘    └──────────┘    └──────────┘
     │               │                │
     ▼               ▼                ▼
┌──────────┐    ┌──────────┐    ┌──────────┐
│ HTTPX    │    │ Base     │    │ PKGBUILD │
│ Client   │    │ Parser   │    │ Editor   │
└──────────┘    └──────────┘    └──────────┘
                              ▲
                              │
                     ┌────────────────┐
                     │ ConfigLoader   │
                     │ (packages.yaml)│
                     └────────────────┘
```

### 分层架构

项目采用经典的**分层架构**模式：

```
┌─────────────────────────────────────────┐
│           表现层 (Presentation)          │  CLI 接口
│         (cli/, main.py)                 │
├─────────────────────────────────────────┤
│            业务逻辑层 (Business)         │  核心协调
│          (core/)                        │
├─────────────────────────────────────────┤
│            数据访问层 (Data Access)      │  数据操作
│  (fetcher/, parsers/, updater/, utils/) │
├─────────────────────────────────────────┤
│          基础设施层 (Infrastructure)     │  配置和常量
│    (constants/, loaders/)               │
└─────────────────────────────────────────┘
```

---

## 核心流程

### 三阶段流程

系统的核心是**Fetch → Parse → Update**三阶段流程：

```
输入: packages.yaml
   │
   ▼
┌─────────────┐
│   配置加载   │  ConfigLoader
└─────────────┘
   │
   ▼
┌─────────────┐
│  阶段1:     │
│   Fetch     │  从网络获取数据
└─────────────┘
   │ 输出: 原始数据
   ▼
┌─────────────┐
│  阶段2:     │
│   Parse     │  解析版本号和URL
└─────────────┘
   │ 输出: 版本号, URL列表
   ▼
┌─────────────┐
│  阶段3:     │
│   Update    │  下载文件, 更新PKGBUILD
└─────────────┘
   │
   ▼
输出: 更新后的 PKGBUILD
```

### 详细流程图

```
开始
  │
  ▼
加载配置 (packages.yaml)
  │
  ├─→ 遍历每个包
  │    │
  │    ▼
  │  [Fetch 阶段]
  │  ┌─────────────────────────┐
  │  │ 1. 从 fetch_url 获取数据  │
  │  │    (Fetcher.fetch_text)  │
  │  └─────────────────────────┘
  │           │
  │           ▼
  │  [Parse 阶段]
  │  ┌─────────────────────────┐
  │  │ 2. 解析版本号             │
  │  │    (Parser.parse_version)│
  │  │ 3. 解析下载 URL           │
  │  │    (Parser.parse_url)     │
  │  └─────────────────────────┘
  │           │
  │           ▼
  │  [验证阶段]
  │  ┌─────────────────────────┐
  │  │ 4. 对比当前版本           │
  │  │    (PKGBUILDEditor.get_pkgver)│
  │  │ 5. 是否需要更新?          │
  │  └─────────────────────────┘
  │           │
  │           ├─ 否 → 跳过
  │           │
  │           └─ 是 → 继续
  │                │
  │                ▼
  │  [下载阶段]
  │  ┌─────────────────────────┐
  │  │ 6. 遍历每个架构           │
  │  │ 7. 下载文件               │
  │  │ 8. 计算校验和 (SHA512)    │
  │  └─────────────────────────┘
  │           │
  │           ▼
  │  [更新阶段]
  │  ┌─────────────────────────┐
  │  │ 9. 更新 pkgver           │
  │  │10. 重置 pkgrel = 1       │
  │  │11. 更新 source_<arch>    │
  │  │12. 更新 sha512sums_<arch>│
  │  │13. 保存 PKGBUILD         │
  │  └─────────────────────────┘
  │
  └─→ 下一个包
       │
       ▼
     结束
```

### 时间线视图

```
时间轴 →

包A:  Fetch → Parse → Download → Update → 完成
包B:           Fetch → Parse → Download → Update → 完成
包C:                     Fetch → Parse → Download → 完成
```

**注**: 当前实现为**串行处理**，未来可优化为并发。

---

## 模块设计

### 1. CLI 模块 (`cli/`)

**职责**: 命令行接口，解析用户输入

**核心类**: 无（纯函数）

**主要函数**:
- `update_main()`: 主入口，处理命令行参数

**依赖**:
- `core.package_updater.PackageUpdater`

**代码示例**:
```python
def update_main():
    parser = argparse.ArgumentParser(description="AUR 包自动更新工具")
    parser.add_argument("--package", help="更新指定包")
    parser.add_argument("--all", action="store_true", help="更新所有包")
    parser.add_argument("--list", action="store_true", help="列出所有包")
    # ...
```

### 2. Core 模块 (`core/`)

**职责**: 核心业务逻辑，协调三个阶段

**核心类**: `PackageUpdater`

**主要方法**:
- `update_package()`: 更新单个包
- `update_all_packages()`: 更新所有包
- `update_single_package()`: 更新指定包

**依赖**:
- `fetcher.Fetcher`
- `parsers.BaseParser` (及其子类)
- `updater.PKGBUILDEditor`
- `loaders.ConfigLoader`

**架构模式**: **门面模式 (Facade)**

### 3. Fetcher 模块 (`fetcher/`)

**职责**: 封装 HTTP 请求，提供数据获取功能

**核心类**: `Fetcher`

**主要方法**:
- `fetch_json()`: 获取 JSON 数据
- `fetch_text()`: 获取文本数据

**技术栈**: `httpx.AsyncClient`

**特点**:
- 异步 I/O
- 自动错误处理
- 可配置超时和请求头

**架构模式**: **适配器模式 (Adapter)**

### 4. Parsers 模块 (`parsers/`)

**职责**: 解析各种格式的数据，提取版本信息

**核心类**:
- `BaseParser`: 抽象基类
- `QQParser`: QQ 解析器实现
- `NavicatPremiumCSParser`: Navicat 解析器实现

**接口**:
```python
class BaseParser(ABC):
    @abstractmethod
    def parse_version(self, response_data) -> str | None:
        """解析版本号"""
        pass

    @abstractmethod
    def parse_url(self, arch, response_data) -> str | None:
        """解析下载 URL"""
        pass
```

**架构模式**: **策略模式 (Strategy)** + **模板方法模式 (Template Method)**

### 5. Updater 模块 (`updater/`)

**职责**: 编辑 PKGBUILD 文件

**核心类**: `PKGBUILDEditor`

**主要方法**:
- `update_pkgver()`: 更新版本号
- `update_pkgrel()`: 更新发布号
- `update_arch_checksum()`: 更新架构校验和
- `update_source_url()`: 更新下载 URL
- `get_pkgver()`: 读取当前版本号

**技术实现**:
- 正则表达式匹配和替换
- 内存编辑，批量保存

**架构模式**: **建造者模式 (Builder)**

### 6. Loaders 模块 (`loaders/`)

**职责**: 加载和验证配置文件

**核心类**:
- `ConfigLoader`: 配置加载器
- `PackageConfig`: 包配置数据模型

**技术栈**:
- `pyyaml`: YAML 解析
- `pydantic`: 数据验证

**架构模式**: **工厂模式 (Factory)**

### 7. Constants 模块 (`constants/`)

**职责**: 定义常量和枚举

**核心内容**:
- `ArchEnum`: 支持的架构
- `HashAlgorithmEnum`: 哈希算法
- `ParserEnum`: 解析器名称
- `NAVICAT_URLS`: URL 映射

**架构模式**: **枚举单例模式 (Enumeration)**

### 8. Utils 模块 (`utils/`)

**职责**: 提供通用工具函数

**核心文件**: `hash.py`

**主要函数**:
- `calculate_file_hash()`: 计算文件哈希
- `verify_file_hash()`: 验证文件哈希
- `download_and_verify()`: 下载并验证

**特点**: 无状态，纯函数

---

## 数据流

### 配置数据流

```
packages.yaml
     │
     ▼
ConfigLoader.load_from_yaml()
     │
     ▼
PackageConfig (Pydantic 模型)
     │
     ├─→ name: str
     ├─→ fetch_url: str
     ├─→ parser: str
     ├─→ arch: List[str]
     └─→ ...
     │
     ▼
PackageUpdater.packages (dict)
```

### 版本数据流

```
网络 (fetch_url)
     │
     ▼
Fetcher.fetch_text()
     │
     ▼
原始数据 (str/JSON)
     │
     ▼
Parser.parse_version()
     │
     ▼
版本号 (str)
     │
     ▼
对比当前版本
     │
     ├─ 相同 → 跳过
     │
     └─ 不同 → 继续
           │
           ▼
     触发更新流程
```

### 下载文件流

```
Parser.parse_url()
     │
     ▼
下载 URL (str)
     │
     ▼
Fetcher.client.get() (httpx)
     │
     ▼
二进制数据 (bytes)
     │
     ▼
写入文件 (downloads/)
     │
     ▼
Hash.calculate_file_hash()
     │
     ▼
SHA512 校验和 (str)
     │
     ▼
更新到 PKGBUILD
```

### PKGBUILD 更新流

```
旧 PKGBUILD
     │
     ▼
PKGBUILDEditor.__init__()
     │
     ▼
加载到内存 (self.content)
     │
     ├─→ update_pkgver()
     ├─→ update_pkgrel()
     ├─→ update_source_url()
     └─→ update_arch_checksum()
          │
          ▼
修改后的内存内容
          │
          ▼
save()
          │
          ▼
写入 PKGBUILD 文件
```

---

## 设计模式

### 1. 门面模式 (Facade)

**应用**: `PackageUpdater`

**目的**: 为复杂的子系统提供简化接口

**实现**:
```python
class PackageUpdater:
    """门面类，隐藏内部复杂性"""
    def __init__(self):
        self.fetcher = Fetcher()           # 子系统
        self.parsers = {...}                # 子系统
        self.config = ConfigLoader.load()   # 子系统

    async def update_package(self, name, config):
        # 简化的接口
        response = await self.fetcher.fetch_text(...)
        version = self.parsers[...].parse_version(response)
        # ...
```

### 2. 策略模式 (Strategy)

**应用**: 解析器系统

**目的**: 定义一系列算法，分别封装，可互换

**实现**:
```python
# 策略接口
class BaseParser(ABC):
    @abstractmethod
    def parse_version(self, data): pass

# 具体策略
class QQParser(BaseParser):
    def parse_version(self, data):
        # QQ 特定策略
        pass

class NavicatParser(BaseParser):
    def parse_version(self, data):
        # Navicat 特定策略
        pass

# 上下文
class PackageUpdater:
    def __init__(self):
        self.parsers = {
            "QQParser": QQParser(),        # 选择策略
            "NavicatParser": NavicatParser(),
        }
```

### 3. 模板方法模式 (Template Method)

**应用**: `BaseParser`

**目的**: 定义算法骨架，子类实现具体步骤

**实现**:
```python
class BaseParser(ABC):
    """模板类"""

    @abstractmethod
    def parse_version(self, data):
        """抽象方法，子类必须实现"""
        pass

    @abstractmethod
    def parse_url(self, arch, data):
        """抽象方法，子类必须实现"""
        pass

class QQParser(BaseParser):
    """实现类"""

    def parse_version(self, data):
        # 具体实现
        pass

    def parse_url(self, arch, data):
        # 具体实现
        pass
```

### 4. 工厂模式 (Factory)

**应用**: `ConfigLoader`

**目的**: 封装对象创建逻辑

**实现**:
```python
class ConfigLoader:
    @classmethod
    def load_from_yaml(cls, filepath: str) -> "ConfigLoader":
        """工厂方法"""
        with open(filepath) as f:
            data = yaml.safe_load(f)
        return cls(**data)
```

### 5. 适配器模式 (Adapter)

**应用**: `Fetcher`

**目的**: 将第三方库接口适配到项目需求

**实现**:
```python
class Fetcher:
    """适配器类"""
    def __init__(self):
        # 被适配对象
        self.client = httpx.AsyncClient()

    async def fetch_json(self, url):
        # 适配接口
        response = await self.client.get(url)
        return response.json()
```

### 6. 建造者模式 (Builder)

**应用**: `PKGBUILDEditor`

**目的**: 分步骤构建复杂对象

**实现**:
```python
editor = PKGBUILDEditor(path)
editor.update_pkgver("1.0.0")       # 步骤1
editor.update_pkgrel(1)             # 步骤2
editor.update_source_url("x86_64", url)  # 步骤3
editor.update_arch_checksum("x86_64", hash)  # 步骤4
editor.save()                       # 步骤5: 构建完成
```

---

## 技术栈

### 核心技术

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.13+ | 编程语言 |
| httpx | latest | 异步 HTTP 客户端 |
| pydantic | latest | 数据验证 |
| pyyaml | latest | YAML 解析 |
| pytest | latest | 测试框架 |
| pytest-asyncio | latest | 异步测试 |

### 为什么选择这些技术？

#### Python 3.13+
- ✅ 最新的类型注解支持
- ✅ 性能提升
- ✅ 现代语法特性

#### httpx (而非 requests)
- ✅ 原生异步支持
- ✅ HTTP/2 支持
- ✅ 请求/响应流

#### pydantic
- ✅ 运行时类型验证
- ✅ 自动类型转换
- ✅ 清晰的错误消息

#### pytest
- ✅ 简洁的语法
- ✅ 强大的 fixture
- ✅ 异步测试支持

---

## 架构决策

### 决策 1: 为什么使用异步 I/O？

**背景**: 需要频繁的网络请求

**选项**:
1. 同步 (requests)
2. 异步 (httpx + asyncio)

**选择**: 异步

**理由**:
- 性能更好，可以并发处理多个请求
- 资源利用率更高
- Python 3.13+ 对异步支持完善

**权衡**:
- 代码复杂度略高
- 调试相对困难

### 决策 2: 为什么使用抽象基类 (ABC)？

**背景**: 需要支持多种解析器

**选项**:
1. 简单函数
2. 抽象基类
3. 协议 (Protocol)

**选择**: 抽象基类

**理由**:
- 强制子类实现接口
- 清晰的继承关系
- 良好的 IDE 支持

**权衡**:
- 必须继承，限制了灵活性

### 决策 3: 为什么使用 Pydantic 数据验证？

**背景**: 需要从 YAML 加载配置

**选项**:
1. 原始字典
2. dataclass
3. Pydantic 模型

**选择**: Pydantic

**理由**:
- 自动类型验证
- 清晰的错误消息
- 支持复杂类型

**权衡**:
- 额外依赖
- 轻微性能开销

### 决策 4: 为什么使用正则表达式编辑 PKGBUILD？

**背景**: 需要更新 PKGBUILD 文件

**选项**:
1. 正则表达式
2. 完整解析器
3. 行号替换

**选择**: 正则表达式

**理由**:
- 简单高效
- PKGBUILD 格式相对固定
- 不需要完整解析

**权衡**:
- 对格式变化敏感
- 可能误匹配

### 决策 5: 为什么串行处理包（而非并发）？

**背景**: 需要更新多个包

**选项**:
1. 串行处理
2. 并发处理

**选择**: 串行（当前实现）

**理由**:
- 实现简单
- 调试容易
- 避免资源争用

**未来优化**:
- 可以使用 `asyncio.gather()` 并发处理
- 需要限制并发数避免过载

---

## 可扩展性

### 添加新包的步骤

1. 在 `packages.yaml` 添加配置
2. 创建解析器类（继承 `BaseParser`）
3. 在 `ParserEnum` 注册
4. 在 `PackageUpdater` 注册

**无需修改核心代码**

### 添加新解析器的步骤

1. 创建解析器类
2. 实现 `parse_version()` 和 `parse_url()`
3. 注册到系统

**符合开闭原则**

### 添加新架构的步骤

1. 在 `ArchEnum` 添加新架构
2. 更新 PKGBUILD 模板
3. 确保解析器支持

**最小化改动**

---

## 性能考虑

### 当前瓶颈

1. **网络 I/O**: 下载文件时间
2. **串行处理**: 一个包完成才处理下一个
3. **哈希计算**: 大文件的 SHA512 计算

### 优化方向

1. **并发下载**: 使用 `asyncio.gather()`
2. **缓存机制**: 缓存版本号，避免重复请求
3. **增量更新**: 只更新有变化的包
4. **流式下载**: 边下载边计算哈希

---

## 安全考虑

### 输入验证

- ✅ Pydantic 验证配置文件
- ✅ 版本号格式验证
- ✅ URL 格式验证

### 文件操作

- ✅ 临时文件隔离
- ✅ 哈希校验防止篡改
- ✅ 原子写入（先写临时文件再重命名）

### 网络安全

- ✅ HTTPS 验证
- ✅ 请求超时限制
- ✅ 用户-Agent 标识

---

**最后更新**: 2026-01-04

# API 参考文档

> 📘 完整的 API 接口文档，包含所有核心类、方法和参数说明

## 目录

- [核心模块](#核心模块)
  - [PackageUpdater](#packageupdater)
  - [ConfigLoader & PackageConfig](#configloader--packageconfig)
- [解析器模块](#解析器模块)
  - [BaseParser](#baseparser)
  - [QQParser](#qqparser)
  - [NavicatPremiumCSParser](#navicatpremiumcsparser)
- [工具模块](#工具模块)
  - [Fetcher](#fetcher)
  - [PKGBUILDEditor](#pkgbuildeditor)
  - [Hash 工具](#hash-工具)
- [枚举类型](#枚举类型)

---

## 核心模块

### PackageUpdater

**位置**: `scripts/core/package_updater.py`

包更新器，整合 Fetch、Parse 和 Update 三个阶段的核心协调器。

#### 初始化

```python
def __init__(self) -> None
```

**功能**:
- 初始化 HTTP 客户端 (Fetcher)
- 加载包配置 (ConfigLoader)
- 注册所有解析器实例
- 设置项目路径

**路径说明**:
- `project_root`: 指向 `scripts/` 目录
- `pkgbuild_root`: 指向项目根目录（用于定位 PKGBUILD 文件）

#### 方法

##### `update_package()`

```python
async def update_package(
    self,
    package_name: str,
    package_config: PackageConfig
) -> bool
```

**功能**: 更新单个包

**参数**:
- `package_name` (str): 包名
- `package_config` (PackageConfig): 包配置对象

**返回值**:
- `bool`: 更新是否成功

**执行流程**:
1. **Fetch 阶段**: 从 `fetch_url` 获取版本信息
2. **Parse 阶段**:
   - 使用指定解析器解析版本号
   - 获取各架构的下载 URL
3. **验证阶段**: 检查当前版本，决定是否需要更新
4. **下载阶段**: 下载各架构的 deb/AppImage 文件
5. **校验阶段**: 计算文件的 SHA512 校验和
6. **更新阶段**: 更新 PKGBUILD 文件
   - 更新 `pkgver`
   - 重置 `pkgrel` 为 1
   - 可选：更新 `source_<arch>` URL
   - 更新各架构的 `sha512sums_<arch>`

**示例**:
```python
updater = PackageUpdater()
success = await updater.update_package("qq", config)
```

##### `update_all_packages()`

```python
async def update_all_packages(self) -> None
```

**功能**: 更新所有配置的包

**行为**:
- 遍历 `packages.yaml` 中的所有包
- 对每个包调用 `update_package()`
- 输出更新成功/失败的统计信息

**示例**:
```python
updater = PackageUpdater()
await updater.update_all_packages()
# 输出: 更新完成: 2/2 个包更新成功
```

##### `update_single_package()`

```python
async def update_single_package(
    self,
    package_name: str
) -> bool
```

**功能**: 更新单个指定的包

**参数**:
- `package_name` (str): 要更新的包名

**返回值**:
- `bool`: 更新是否成功

**错误处理**:
- 如果包名不在配置中，返回 `False` 并输出错误信息

**示例**:
```python
updater = PackageUpdater()
success = await updater.update_single_package("qq")
```

##### `list_available_packages()`

```python
def list_available_packages(self) -> None
```

**功能**: 列出所有可用的包

**示例**:
```python
updater = PackageUpdater()
updater.list_available_packages()
# 输出:
# 可用的包:
#   - qq
#   - navicat
```

##### `_get_pkgbuild_path()`

```python
def _get_pkgbuild_path(
    self,
    pkgbuild_relative_path: str
) -> Path
```

**功能**: 获取 PKGBUILD 文件的完整路径

**参数**:
- `pkgbuild_relative_path` (str): PKGBUILD 的相对路径

**返回值**:
- `Path`: PKGBUILD 的完整路径

**路径处理逻辑**:
- 支持绝对路径和相对路径
- 相对路径基于 `pkgbuild_root`（项目根目录）

##### `_download_file()`

```python
async def _download_file(
    self,
    url: str,
    file_path: Path
) -> bool
```

**功能**: 下载文件到指定路径

**参数**:
- `url` (str): 下载 URL
- `file_path` (Path): 保存路径

**返回值**:
- `bool`: 下载是否成功

##### `_calculate_checksum()`

```python
async def _calculate_checksum(
    self,
    file_path: Path
) -> str
```

**功能**: 计算文件的 SHA512 校验和

**参数**:
- `file_path` (Path): 文件路径

**返回值**:
- `str`: SHA512 校验和（十六进制字符串）

---

### ConfigLoader & PackageConfig

**位置**: `scripts/loaders/config_loader.py`

#### PackageConfig

包配置数据模型，使用 Pydantic 进行数据验证。

**字段**:

| 字段名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `name` | str | ✅ | - | 包名 |
| `source` | str | ✅ | - | 来源标识 |
| `source_url` | str | ✅ | - | 官方网站 URL |
| `fetch_url` | str | ✅ | - | 获取版本信息的 URL |
| `upstream` | str | ✅ | - | 上游项目 |
| `parser` | str | ✅ | - | 解析器名称（必须匹配 ParserEnum） |
| `pkgbuild` | str | ✅ | - | PKGBUILD 文件相对路径 |
| `arch` | List[str] | ❌ | [] | 支持的架构列表 |
| `update_source_url` | bool | ❌ | True | 是否更新 source URL |

**方法**:

##### `get_supported_archs()`

```python
def get_supported_archs(self) -> List[ArchEnum]
```

**功能**: 将字符串架构列表转换为 `ArchEnum` 列表

**返回值**:
- `List[ArchEnum]`: 支持的架构枚举列表

**示例**:
```python
config = PackageConfig(
    name="qq",
    arch=["x86_64", "aarch64", "loong64"],
    ...
)
archs = config.get_supported_archs()
# 返回: [ArchEnum.X86_64, ArchEnum.AARCH64, ArchEnum.LOONG64]
```

#### ConfigLoader

配置加载器，从 YAML 文件加载包配置。

**字段**:
- `packages` (dict[str, PackageConfig]): 包名到配置的映射

**类方法**:

##### `load_from_yaml()`

```python
@classmethod
def load_from_yaml(
    cls,
    filepath: str = "packages.yaml"
) -> "ConfigLoader"
```

**功能**: 从 YAML 文件加载配置

**参数**:
- `filepath` (str): YAML 文件路径，默认为 `packages.yaml`

**返回值**:
- `ConfigLoader`: 配置加载器实例

**异常处理**:
- 文件不存在会抛出 `FileNotFoundError`
- YAML 格式错误会抛出 `yaml.YAMLError`
- 数据验证失败会抛出 `pydantic.ValidationError`

**示例**:
```python
loader = ConfigLoader.load_from_yaml("packages.yaml")
config = loader.packages["qq"]
print(config.fetch_url)
```

---

## 解析器模块

### BaseParser

**位置**: `scripts/parsers/base_parser.py`

所有解析器的抽象基类，定义了解析器必须实现的接口。

#### 抽象方法

##### `parse_version()`

```python
@abstractmethod
def parse_version(
    self,
    response_data: str | Any
) -> str | None
```

**功能**: 从响应数据中提取版本号

**参数**:
- `response_data` (str | Any): API 响应数据，通常是文本或 JSON

**返回值**:
- `str | None`: 版本号字符串，解析失败返回 `None`

**实现要点**:
- 版本号格式应遵循语义化版本规范（如 `1.2.3`）
- 处理各种可能的响应格式（HTML、JSON、JavaScript 等）
- 无法解析时应返回 `None`

##### `parse_url()`

```python
@abstractmethod
def parse_url(
    self,
    arch: ArchEnum | str,
    response_data: str | Any
) -> str | None
```

**功能**: 从响应数据中提取指定架构的下载 URL

**参数**:
- `arch` (ArchEnum | str): 目标架构
- `response_data` (str | Any): API 响应数据

**返回值**:
- `str | None`: 下载 URL，解析失败返回 `None`

**实现要点**:
- 支持多架构（x86_64, aarch64, loong64 等）
- URL 应指向 deb 或 AppImage 文件
- 处理相对 URL 和绝对 URL

#### 使用示例

```python
from abc import ABC, abstractmethod

class MyCustomParser(BaseParser):
    def parse_version(self, response_data):
        # 从 HTML 中提取版本号
        match = re.search(r'version["\s:]+(\d+\.\d+\.\d+)', response_data)
        return match.group(1) if match else None

    def parse_url(self, arch, response_data):
        # 从 JSON 中提取下载 URL
        data = json.loads(response_data)
        return data.get("downloads", {}).get(arch.value)
```

---

### QQParser

**位置**: `scripts/parsers/qq.py`

QQ Linux 包解析器，从腾讯的配置文件中提取版本信息。

**数据源**:
- Fetch URL: `https://cdn-go.cn/qq-web/im.qq.com_new/latest/rainbow/linuxConfig.js`
- 格式: JavaScript 对象

**实现特点**:
- 解析 JavaScript 配置文件
- 提取 `linux.qq.version` 字段
- 构造下载 URL: `https://dldir1.qq.com/qqfile/qq/QQNT/Linux/QQ_{version}_{arch}.deb`

**支持架构**:
- x86_64
- aarch64
- loong64

---

### NavicatPremiumCSParser

**位置**: `scripts/parsers/navicat.py`

Navicat Premium 包解析器，从官方发布说明中提取版本信息。

**数据源**:
- Fetch URL: `https://www.navicat.com.cn/products/navicat-premium-release-note#L`
- 格式: HTML

**实现特点**:
- 解析 HTML 发布说明页面
- 从发布列表中提取最新版本号
- 使用预定义的 URL 映射（`NAVICAT_URLS`）

**支持架构**:
- x86_64: AppImage 格式
- aarch64: AppImage 格式

**注意事项**:
- 不更新 source URL（`update_source_url: false`）
- 下载 URL 固定，不需要动态解析

---

## 工具模块

### Fetcher

**位置**: `scripts/fetcher/fetcher.py`

HTTP 客户端封装，提供异步的网络请求功能。

#### 初始化

```python
def __init__(
    self,
    timeout: int = 10,
    headers: dict[str, str] | None = None
) -> None
```

**参数**:
- `timeout` (int): 请求超时时间（秒），默认 10
- `headers` (dict | None): 自定义 HTTP 头，默认为 `None`

**默认请求头**:
```python
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 ...",
    "Accept": "*/*",
    "Cache-Control": "no-cache",
}
```

#### 方法

##### `fetch_json()`

```python
async def fetch_json(
    self,
    url: str,
    headers: dict[str, str] | None = None
) -> Any | None
```

**功能**: 请求 URL 并返回 JSON 数据

**参数**:
- `url` (str): 请求的 URL
- `headers` (dict | None): 额外的请求头

**返回值**:
- `Any | None`: 解析后的 JSON 数据，失败返回 `None`

**错误处理**:
- 任何异常都会捕获并打印错误信息
- 返回 `None` 表示请求失败

**示例**:
```python
fetcher = Fetcher()
data = await fetcher.fetch_json("https://api.github.com/repos/user/repo/releases/latest")
if data:
    print(data["tag_name"])
```

##### `fetch_text()`

```python
async def fetch_text(
    self,
    url: str,
    headers: dict[str, str] | None = None
) -> str | None
```

**功能**: 请求 URL 并返回文本数据

**参数**:
- `url` (str): 请求的 URL
- `headers` (dict | None): 额外的请求头

**返回值**:
- `str | None`: 响应文本，失败返回 `None`

**示例**:
```python
fetcher = Fetcher()
html = await fetcher.fetch_text("https://example.com")
if html:
    print(html[:100])  # 打印前 100 个字符
```

---

### PKGBUILDEditor

**位置**: `scripts/updater/pkgbuild_editor.py`

PKGBUILD 文件编辑器，使用正则表达式更新版本、校验和等字段。

#### 初始化

```python
def __init__(self, pkgbuild_path: Path) -> None
```

**参数**:
- `pkgbuild_path` (Path): PKGBUILD 文件路径

**行为**:
- 自动加载文件内容到内存
- 所有操作先在内存中修改，调用 `save()` 才会写入文件

#### 读取方法

##### `get_pkgver()`

```python
def get_pkgver(self) -> str
```

**功能**: 获取当前 `pkgver` 值

**返回值**:
- `str`: 当前的 pkgver 值

**示例**:
```python
editor = PKGBUILDEditor(Path("PKGBUILD"))
version = editor.get_pkgver()
print(f"当前版本: {version}")
```

##### `get_pkgrel()`

```python
def get_pkgrel(self) -> int
```

**功能**: 获取当前 `pkgrel` 值

**返回值**:
- `int`: 当前的 pkgrel 值

##### `get_epoch()`

```python
def get_epoch(self) -> int | None
```

**功能**: 获取当前 `epoch` 值

**返回值**:
- `int | None`: 当前的 epoch 值，不存在则返回 `None`

##### `get_checksum()`

```python
def get_checksum(
    self,
    arch: str | None = None
) -> str
```

**功能**: 获取当前 sha512sums 值

**参数**:
- `arch` (str | None): 架构名称，`None` 表示通用校验和

**返回值**:
- `str`: 当前的校验和值

#### 更新方法

##### `update_pkgver()`

```python
def update_pkgver(self, new_version: str) -> None
```

**功能**: 更新 `pkgver` 字段

**参数**:
- `new_version` (str): 新版本号

**正则表达式**:
```python
pattern = r"^pkgver=.*$"
replacement = f"pkgver={new_version}"
```

##### `update_pkgrel()`

```python
def update_pkgrel(self, new_pkgrel: int = 1) -> None
```

**功能**: 更新 `pkgrel` 字段

**参数**:
- `new_pkgrel` (int): 新的发布号，默认为 1

**注意**: 版本更新时应重置为 1

##### `update_epoch()`

```python
def update_epoch(self, new_epoch: int | None = None) -> None
```

**功能**: 更新或添加 `epoch` 字段

**参数**:
- `new_epoch` (int | None): 新的 epoch 值，`None` 则不更新

**行为**:
- 字段存在：更新值
- 字段不存在：在 `pkgver` 之前插入

##### `update_sha512sums()`

```python
def update_sha512sums(self, new_checksum: str) -> None
```

**功能**: 更新通用 `sha512sums` 字段

**参数**:
- `new_checksum` (str): 新的 SHA512 校验和

##### `update_arch_checksum()`

```python
def update_arch_checksum(
    self,
    arch: str,
    new_checksum: str,
    hash_algorithm: str = HashAlgorithmEnum.SHA512.value
) -> None
```

**功能**: 更新特定架构的校验和字段

**参数**:
- `arch` (str): 架构名称（如 'x86_64', 'aarch64'）
- `new_checksum` (str): 新的校验和
- `hash_algorithm` (str): 哈希算法，默认 'sha512'

**字段格式**:
```bash
sha512sums_x86_64=('abc123...')
sha512sums_aarch64=('def456...')
```

##### `update_source_url()`

```python
def update_source_url(self, arch: str, new_url: str) -> None
```

**功能**: 更新特定架构的 source URL

**参数**:
- `arch` (str): 架构名称
- `new_url` (str): 新的源码 URL

**字段格式**:
```bash
source_x86_64=('https://example.com/file_x86_64.deb')
source_aarch64=('https://example.com/file_aarch64.deb')
```

#### 批量操作

##### `update_all()`

```python
def update_all(
    self,
    new_version: str,
    new_checksums: dict[str, str],
    new_urls: dict[str, str],
    new_pkgrel: int = 1,
    new_epoch: int | None = None,
    generic_checksum: str | None = None,
    hash_algorithm: str = HashAlgorithmEnum.SHA512.value
) -> None
```

**功能**: 一次性更新所有相关字段

**参数**:
- `new_version` (str): 新版本号
- `new_checksums` (dict[str, str]): 各架构的校验和
- `new_urls` (dict[str, str]): 各架构的源码 URL
- `new_pkgrel` (int): 新的发布号
- `new_epoch` (int | None): 新的 epoch 值
- `generic_checksum` (str | None): 通用的校验和
- `hash_algorithm` (str): 哈希算法

**示例**:
```python
editor.update_all(
    new_version="1.2.3",
    new_checksums={
        "x86_64": "abc123...",
        "aarch64": "def456..."
    },
    new_urls={
        "x86_64": "https://example.com/file_x86_64.deb",
        "aarch64": "https://example.com/file_aarch64.deb"
    }
)
editor.save()
```

#### 文件操作

##### `save()`

```python
def save(self) -> None
```

**功能**: 保存所有更改到 PKGBUILD 文件

##### `reload()`

```python
def reload(self) -> None
```

**功能**: 重新加载 PKGBUILD 文件，放弃所有未保存的更改

---

### Hash 工具

**位置**: `scripts/utils/hash.py`

哈希计算工具函数集。

#### 主要函数

##### `calculate_file_hash()`

```python
def calculate_file_hash(
    file_path: Union[str, Path],
    algorithm: str = "sha512"
) -> str
```

**功能**: 计算文件的哈希值

**参数**:
- `file_path` (str | Path): 文件路径
- `algorithm` (str): 哈希算法（'md5', 'sha1', 'sha256', 'sha512'）

**返回值**:
- `str`: 十六进制哈希值

##### `calculate_sha256()`

```python
def calculate_sha256(file_path: Union[str, Path]) -> str
```

**功能**: 计算文件的 SHA256 哈希值

##### `calculate_multiple_hashes()`

```python
def calculate_multiple_hashes(
    file_path: Union[str, Path],
    algorithms: List[str]
) -> Dict[str, str]
```

**功能**: 一次性计算多种哈希算法

**返回值**:
- `Dict[str, str]`: 算法名到哈希值的映射

##### `verify_file_hash()`

```python
def verify_file_hash(
    file_path: Union[str, Path],
    expected_hash: str,
    algorithm: str = "sha512"
) -> bool
```

**功能**: 验证文件的哈希值是否匹配

**参数**:
- `expected_hash` (str): 预期的哈希值

**返回值**:
- `bool`: 是否匹配

##### `download_and_verify()`

```python
async def download_and_verify(
    url: str,
    destination: Union[str, Path],
    expected_hash: str,
    algorithm: str = "sha512"
) -> bool
```

**功能**: 下载文件并验证哈希值

**参数**:
- `url` (str): 下载 URL
- `destination` (str | Path): 保存路径
- `expected_hash` (str): 预期的哈希值

**返回值**:
- `bool`: 下载成功且哈希值匹配

---

## 枚举类型

### ArchEnum

**位置**: `scripts/constants/constants.py`

支持的 CPU 架构枚举。

**值**:
```python
class ArchEnum(Enum):
    X86_64 = "x86_64"
    AARCH64 = "aarch64"
    LOONG64 = "loong64"
    MIPS64EL = "mips64el"
```

**使用示例**:
```python
# 获取枚举值
arch = ArchEnum.X86_64
print(arch.value)  # 输出: x86_64

# 从字符串获取枚举
arch = ArchEnum("x86_64")
```

---

### HashAlgorithmEnum

**位置**: `scripts/constants/constants.py`

哈希算法枚举。

**值**:
```python
class HashAlgorithmEnum(Enum):
    SHA256 = "sha256"
    SHA512 = "sha512"
```

**类方法**:

##### `get_all()`

```python
@classmethod
def get_all(cls) -> List[str]
```

**功能**: 获取所有支持的哈希算法

**返回值**:
- `List[str]`: 算法名称列表

**示例**:
```python
algorithms = HashAlgorithmEnum.get_all()
# 返回: ['sha256', 'sha512']
```

---

### ParserEnum

**位置**: `scripts/constants/constants.py`

解析器名称枚举，用于映射配置文件中的解析器名称到实际类。

**值**:
```python
class ParserEnum(Enum):
    QQ = "QQParser"
    NAVICAT_PREMIUM_CS = "NavicatPremiumCSParser"
```

**使用场景**:
- 在 `packages.yaml` 中指定解析器
- 在 `PackageUpdater` 中注册解析器实例

**示例**:
```python
# 在配置文件中
parser: QQParser

# 在代码中注册
self.parsers: dict[str, BaseParser] = {
    ParserEnum.QQ.value: QQParser(),
    ParserEnum.NAVICAT_PREMIUM_CS.value: NavicatPremiumCSParser(),
}
```

---

### PackageEnum

**位置**: `scripts/constants/constants.py`

包名称枚举。

**值**:
```python
class PackageEnum(Enum):
    QQ = "qq"
    NAVICAT_PREMIUM_CS = "navicat-premium-cs"
```

**用途**:
- 标准化包名称
- 避免硬编码字符串

---

## 类型注解

项目中广泛使用 Python 类型注解，主要类型：

- `str | None`: 可选字符串
- `dict[str, str]`: 字符串到字符串的字典
- `List[str]`: 字符串列表
- `Path`: 路径对象（来自 `pathlib`）
- `Union[str, Path]`: 字符串或路径对象
- `Any`: 任意类型

---

## 错误处理

### 异常类型

项目不使用自定义异常类，主要依赖 Python 内置异常：

- `FileNotFoundError`: 文件不存在
- `ValueError`: 值错误（如枚举值无效）
- `yaml.YAMLError`: YAML 解析错误
- `pydantic.ValidationError`: 数据验证错误

### 错误处理模式

```python
# Fetcher: 返回 None 表示失败
data = await fetcher.fetch_json(url)
if not data:
    print("获取数据失败")
    return False

# PackageUpdater: 捕获所有异常
try:
    response = await self.fetcher.fetch_text(url)
except Exception as e:
    print(f"发生异常: {e}")
    return False
```

---

**最后更新**: 2026-01-04

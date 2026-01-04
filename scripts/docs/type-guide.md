# 类型注解与 Ty 检查指南

本指南整合了类型注解使用规范和 Ty 类型检查器的使用方法。

## 目录

1. [类型注解规范](#类型注解规范)
2. [Ty 类型检查器](#ty-类型检查器)
3. [快速参考](#快速参考)
4. [常见问题](#常见问题)

---

## 类型注解规范

### 基本规则

#### 1. 所有函数必须有类型注解

```python
# ✓ 正确
def greet(name: str) -> str:
    return f"Hello, {name}"

# ✗ 错误（缺少返回类型）
def greet(name: str):
    return f"Hello, {name}"
```

#### 2. 使用 Python 3.13+ 现代语法

```python
# ✓ 使用 | 联合类型
def parse(data: str | None) -> str | None:
    return data.upper() if data else None

# ✓ 使用内置泛型
def get_items() -> list[str]:
    return ["a", "b", "c"]

# ✗ 避免（旧式语法）
from typing import Union, List
def parse(data: Union[str, None]) -> Union[str, None]:
    ...
```

#### 3. 类的类型注解

```python
class PackageUpdater:
    parsers: dict[str, BaseParser]  # 类属性

    def __init__(self) -> None:  # __init__ 返回 None
        self.config: ConfigLoader = ConfigLoader()

    def update(self, name: str) -> bool:
        return True
```

#### 4. 异步函数

```python
async def fetch_data(url: str) -> str | None:
    """获取远程数据"""
    try:
        return await client.get(url)
    except Exception:
        return None
```

### 复杂类型

```python
from typing import Callable

# Callable 类型
def apply(
    data: list[str],
    func: Callable[[str], str],  # (参数) -> 返回值
) -> list[str]:
    return [func(item) for item in data]

# 字面量类型
from typing import Literal

def configure(mode: Literal["debug", "release"]) -> None:
    pass
```

---

## Ty 类型检查器

### 简介

**Ty** 是 Astral（uv 的开发团队）创建的极速 Python 类型检查器，使用 Rust 编写。

### 优势

| 特性 | Ty | Pyright | mypy |
|------|-----|---------|------|
| 速度 | ⚡⚡⚡ 极快 | ⚡⚡ 快 | ⚡ 一般 |
| 准确性 | ✅ 精准 | ✅ 精准 | ✅ 精准 |
| Python 3.13+ | ✅ 完整支持 | ✅ 完整支持 | ⚠️ 部分 |
| Rust 实现 | ✅ | ❌ | ❌ |
| uv 集成 | ✅ 原生支持 | ❌ | ❌ |

### 基本使用

```bash
# 检查整个项目
uv run ty check

# 检查特定目录
uv run ty check scripts/core/
uv run ty check loaders/ utils/

# 详细输出
uv run ty check -v

# 监视模式（自动重新检查）
uv run ty check --watch

# 不同输出格式
uv run ty check --output-format concise
uv run ty check --output-format github  # GitHub Actions 格式
```

### 配置

在 `pyproject.toml` 中配置：

```toml
[tool.ty]
# Ty 配置

[tool.ty.src]
# 排除的文件和目录
exclude = [
    ".venv",
    "__pycache__",
    "*.pyc",
]

[tool.ty.analysis]
# 尊重 type: ignore 注释
respect-type-ignore-comments = true

[tool.ty.terminal]
# 输出格式：full, concise, gitlab, github
output-format = "full"

# 将警告视为错误
error-on-warning = false
```

### 高级选项

```bash
# 覆盖配置
uv run ty check --config "output-format=concise"

# 排除特定文件
uv run ty check --exclude "tests/*"

# 启用/禁用规则
uv run ty check --warn unused-variable
uv run ty check --ignore missing-imports
```

---

## 快速参考

### 开发工作流

1. **编写代码**：确保所有函数都有完整的类型注解
2. **类型检查**：`uv run ty check`
3. **修复错误**：根据 ty 的提示修复类型错误
4. **提交代码**：确保所有检查都通过

### 常用命令

```bash
# 基本检查
uv run ty check

# 详细模式
uv run ty check -v
uv run ty check -vv  # 更详细

# 监视模式
uv run ty check --watch

# 排除文件
uv run ty check --exclude "tests/*" --exclude "**/legacy.py"
```

### VS Code 集成

1. 安装 Ty：`uv add --dev ty`
2. 启动 LSP：`uv run ty server`
3. 配置编辑器连接到 Ty LSP

### CI/CD 集成

在 `.github/workflows/python.yml` 中：

```yaml
name: Type Check

on: [push, pull_request]

jobs:
  type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      - name: Install dependencies
        run: uv sync
      - name: Run Ty
        run: uv run ty check
```

---

## 常见问题

### Q: 何时使用 `str | None` vs `Optional[str]`？

A: 在 Python 3.10+ 中，优先使用 `str | None`，更简洁直观。

```python
# ✓ 推荐（Python 3.10+）
def func(value: str | None) -> None:
    pass

# ✓ 可接受（向后兼容）
from typing import Optional
def func(value: Optional[str]) -> None:
    pass
```

### Q: 如何注解回调函数？

A: 使用 `Callable` 类型：

```python
from typing import Callable

def on_event(
    callback: Callable[[str, int], None]  # (参数类型) -> 返回类型
) -> None:
    callback("event", 42)
```

### Q: 如何处理自引用类型？

A: 使用字符串前向引用：

```python
class Node:
    def __init__(self) -> None:
        self.children: list[Node] = []  # ✓ Python 3.7+
```

### Q: Ty 报告找不到模块怎么办？

```bash
# 确保依赖已安装
uv sync

# 检查 Python 环境
uv run ty check --python .venv/bin/python
```

### Q: 如何临时忽略类型错误？

```python
# 不推荐（仅作为最后手段）
value: int = some_untyped_function()  # type: ignore
```

### Q: 类型检查失败如何处理？

1. 检查所有函数是否有返回类型注解
2. 确保所有参数都有类型注解
3. 查看详细的错误信息：`uv run ty check -v`
4. 修复类型错误而不是忽略

---

## 更多资源

- [Python 类型注解官方文档](https://docs.python.org/zh-cn/3/library/typing.html)
- [Ty 官方文档](https://docs.astral.sh/ty/)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [PEP 585 - Type Hinting Generics](https://peps.python.org/pep-0585/)
- [PEP 613 - Explicit Type Aliases](https://peps.python.org/pep-0613/)

---

**最后更新**：2025-01-04
**维护者**：Claude Code

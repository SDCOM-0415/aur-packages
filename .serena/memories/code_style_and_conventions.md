# 代码风格和约定

## 类型注解（Type Hints）- 严格执行
项目**严格使用类型注解**，所有函数和方法必须包含完整的参数和返回类型注解。

### 基本规则

1. **所有函数必须有返回类型注解**
   ```python
   # ✓ 正确
   def get_version(url: str) -> str | None:
       ...

   # ✗ 错误
   def get_version(url: str):
       ...
   ```

2. **使用 Python 3.13+ 现代类型注解语法**
   ```python
   # ✓ 使用 | 联合类型
   def parse_version(data: str | None) -> str | None:
       ...

   # ✓ 使用 list/dict 泛型
   def get_urls(arch: str) -> list[str]:
       return []
   ```

3. **避免旧式 typing 模块语法**（除非必要）
   ```python
   # ✗ 避免
   from typing import List, Dict, Optional
   def parse_version(data: Optional[str]) -> Optional[str]:
       ...
   ```

## 导入规则
- 使用**绝对导入**（`from cli.cli import update_main`）
- 避免相对导入

## 命名约定
- **类名**: PascalCase (`PackageUpdater`, `BaseParser`)
- **函数/方法**: snake_case (`parse_version`, `update_package`)
- **常量**: UPPER_SNAKE_CASE (`ParserEnum`, `ArchEnum`)
- **变量**: snake_case (`pkgbuild_root`, `project_root`)

## 类属性和方法注解
```python
class PackageUpdater:
    parsers: dict[str, BaseParser]  # 类属性类型注解

    def __init__(self) -> None:  # __init__ 返回 None
        self.config: ConfigLoader = ConfigLoader.load_from_yaml()
```

## 异步函数
```python
async def fetch_text(url: str) -> str | None:
    ...

async def download_all(urls: dict[str, str]) -> dict[str, bool]:
    ...
```

## 抽象基类
- 使用 `ABC` 和 `@abstractmethod` 装饰器
- 抽象方法使用 `pass` 作为占位符

## 路径处理
- 使用 `pathlib.Path` 对象处理文件路径
- 支持相对和绝对路径

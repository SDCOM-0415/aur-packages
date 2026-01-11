# 常用命令

## 开发命令（使用 uv）

### 运行程序
```bash
cd scripts
uv run main.py                    # 更新所有包
uv run main.py --all              # 更新所有包（显式）
uv run main.py --package qq       # 更新指定包
uv run main.py --list             # 列出所有可用包
```

### 测试
```bash
uv run pytest                     # 运行所有测试
uv run pytest tests/              # 运行所有测试
uv run pytest tests/fetcher/test_fetcher.py  # 运行单个测试文件
```

### 依赖管理
```bash
uv sync                           # 同步依赖
uv add <package>                  # 添加新依赖
uv remove <package>               # 移除依赖
```

## 类型检查
```bash
uv run ty check                   # 运行类型检查
uv run ty check scripts/core/     # 检查特定目录
uv run ty check -v                # 详细输出
uv run ty check --watch           # 监视模式
```

## 代码格式化
```bash
uv run ruff check                 # 检查代码
uv run ruff format                # 格式化代码
```

## 系统命令（Windows）
```bash
# Git
git status
git diff
git add .
git commit -m "message"

# 目录导航
cd scripts                       # 进入目录
cd ..                            # 返回上级目录
dir                              # 列出目录内容（Windows 版 ls）

# 文件操作
type file.txt                    # 查看文件内容（Windows 版 cat）
```

## 重要约定
- **禁止显式使用 `python` 命令**，统一使用 `uv run`
- 所有命令必须在 `scripts/` 目录下执行（或使用 `cd scripts` 进入）

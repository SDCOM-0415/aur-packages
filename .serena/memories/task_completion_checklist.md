# 任务完成检查清单

## 代码修改后必须执行

### 1. 类型检查
```bash
uv run ty check
```
- 项目使用 **ty** 进行静态类型检查
- 必须确保所有类型注解正确

### 2. 代码格式检查
```bash
uv run ruff check
uv run ruff format
```

### 3. 运行测试
```bash
uv run pytest
```
- 确保所有测试通过
- 如有新增功能，添加相应测试

### 4. 类型注解验证
- 检查所有新增函数是否有：
  - 参数类型注解
  - 返回类型注解
- 使用 Python 3.13+ 现代语法 (`str | None` 而非 `Optional[str]`)

## 添加新软件包检查清单

1. 在 `packages.yaml` 中添加包配置
2. 在 `parsers/` 中创建新的解析器类，继承 `BaseParser`
3. 在 `constants/constants.py` 的 `ParserEnum` 中添加解析器名称
4. 在 `core/package_updater.py` 中注册解析器实例
5. 在 `packages/` 目录中创建对应的 PKGBUILD 文件
6. 添加相应的测试用例

## 提交前检查
- [ ] 类型检查通过 (`uv run ty check`)
- [ ] 代码格式化完成 (`uv run ruff format`)
- [ ] 所有测试通过 (`uv run pytest`)
- [ ] 新功能有对应测试
- [ ] 类型注解完整

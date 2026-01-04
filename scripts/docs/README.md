# 项目文档

本目录包含 AUR 包自动更新工具的完整文档。

## 📚 文档目录

### 核心文档

1. **[类型注解与 Ty 检查指南](./type-guide.md)** ⭐ 必读
   - Python 类型注解完整规范
   - Ty 类型检查器使用说明
   - 快速参考和常见问题
   - 开发工作流和最佳实践

2. **[Downloader 优化文档](./downloader.md)** ⭐ 推荐
   - 下载器优化总结和代码对比
   - TaskGroup 和指数退避重试
   - API 变更和使用示例
   - 性能提升和技术栈

## 📖 文档结构

```
docs/
├── README.md     # 本文档（文档索引）
├── type-guide.md # 类型注解与 Ty 检查统一指南
└── downloader.md # Downloader 优化文档
```

## 🎯 快速导航

### 对于新用户

1. 首先阅读项目根目录的 [CLAUDE.md](../CLAUDE.md) 了解项目概况
2. 查看 **[类型注解指南](./type-guide.md)** 了解代码规范
3. 学习项目架构和开发流程

### 对于开发者

1. **代码规范**：阅读 **[类型注解指南](./type-guide.md)**
2. **类型检查**：运行 `uv run ty check`
3. **下载器优化**：查看 **[Downloader 文档](./downloader.md)**

### 对于维护者

1. **架构理解**：阅读 [CLAUDE.md](../CLAUDE.md) 的架构设计部分
2. **改进历史**：查看 **[Downloader 文档](./downloader.md)**
3. **代码规范**：遵循 **[类型注解指南](./type-guide.md)**

## 📊 文档统计

| 文档 | 大小 | 重要性 | 更新时间 |
|------|------|--------|----------|
| type-guide.md | 6.0KB | ⭐⭐⭐ | 2025-01-04 |
| downloader.md | 5.1KB | ⭐⭐⭐ | 2025-01-04 |

## 🛠️ 维护指南

### 添加新文档

1. 使用清晰的 Markdown 格式
2. 包含适当的代码示例
3. 添加目录和交叉引用
4. 在本 README 中注册

### 更新文档

1. 保持文档与代码同步
2. 更新版本变更
3. 添加新的最佳实践
4. 修正错误和不准确之处

### 文档命名规范

- 使用小写字母和连字符：`document-name.md`
- 名称应描述内容：`type-guide.md`
- 避免使用特殊字符和空格

## 📝 文档风格

### Markdown 规范

- 使用 ATX 风格标题（`#` 标记）
- 代码块指定语言：\```python
- 列表使用 `-` 标记
- 链接使用描述文本：[文本](URL)

### 代码示例

所有代码示例应：
- 简洁明了
- 包含必要注释
- 符合项目代码规范
- 可直接运行或验证

### 文档语言

- 主要使用中文编写
- 技术术语保留英文
- 代码注释使用英文

## 🔗 相关资源

### 项目文档

- [CLAUDE.md](../CLAUDE.md) - 项目概览和开发指南
- [pyproject.toml](../pyproject.toml) - 项目配置和依赖
- [packages.yaml](../packages.yaml) - 包配置文件

### 外部资源

- [Python 3.13 文档](https://docs.python.org/3.13/)
- [Ty 类型检查器](https://docs.astral.sh/ty/)
- [httpx 文档](https://www.python-httpx.org/)
- [Pydantic 文档](https://docs.pydantic.dev/)

## 💡 贡献指南

欢迎改进文档！请注意：

1. 保持文档简洁明了
2. 使用一致的格式和风格
3. 添加实际可用的示例
4. 及时更新过时内容

## 📧 反馈

如有问题或建议，请：
- 提交 Issue
- 发起 Pull Request
- 联系维护者

---

**最后更新**：2025-01-04
**维护者**：Claude Code

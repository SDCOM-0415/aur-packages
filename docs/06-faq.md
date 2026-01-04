# 常见问题

> ❓ 常见问题解答，帮助你快速解决使用中的问题

## 目录

- [安装与配置](#安装与配置)
- [使用问题](#使用问题)
- [更新与维护](#更新与维护)
- [错误处理](#错误处理)
- [性能优化](#性能优化)
- [扩展开发](#扩展开发)

---

## 安装与配置

### Q1: Python 版本不满足要求怎么办？

**问题描述**:
```
错误: Python 3.13+ is required
当前版本: Python 3.11.5
```

**解决方案**:

#### Arch Linux
```bash
# 安装最新版 Python
sudo pacman -S python

# 验证版本
uv run python --version
```

#### Ubuntu/Debian
```bash
# 使用 deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.13
```

#### 使用 pyenv (推荐)
```bash
# 安装 pyenv
curl https://pyenv.run | bash

# 安装 Python 3.13
pyenv install 3.13.0

# 设置为默认版本
pyenv global 3.13.0
```

### Q2: 依赖安装失败怎么办？

**问题描述**:
```
错误: 无法安装 httpx 或其他依赖
```

**解决方案**:

#### 使用 uv (推荐)
```bash
# 安装 uv
pip install uv

# 同步依赖
cd scripts
uv sync
```

#### 使用 pip (不推荐)
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 升级 pip
pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt
```

**注意**: 项目统一使用 `uv` 管理和运行，上述方法仅作备用参考。

#### 网络问题
```bash
# 使用国内镜像源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 或临时使用
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple httpx
```

### Q3: 配置文件找不到怎么办？

**问题描述**:
```
错误: packages.yaml 不存在
```

**解决方案**:

```bash
# 1. 确认当前目录
pwd
# 应该在 .../aur-packages/scripts

# 2. 检查文件是否存在
ls -la packages.yaml

# 3. 如果不存在，创建示例配置
cat > packages.yaml << 'EOF'
packages:
  example:
    name: example
    source: example
    source_url: "https://example.com"
    fetch_url: "https://api.example.com/version"
    upstream: "user/repo"
    parser: ExampleParser
    pkgbuild: "packages/example/PKGBUILD"
    update_source_url: true
    arch:
      - x86_64
EOF
```

---

## 使用问题

### Q4: 如何只检查版本而不更新？

**问题描述**: 想要查看最新版本，但不修改 PKGBUILD

**解决方案**:

创建一个检查脚本 `check_version.py`:

```python
import asyncio
from core.package_updater import PackageUpdater

async def check_versions():
    updater = PackageUpdater()

    for name, config in updater.config.packages.items():
        print(f"\n检查包: {name}")
        print(f"  数据源: {config.fetch_url}")

        # 获取版本信息
        response = await updater.fetcher.fetch_text(config.fetch_url)
        if not response:
            print(f"  错误: 无法获取数据")
            continue

        # 解析版本
        parser = updater.parsers.get(config.parser)
        if not parser:
            print(f"  错误: 找不到解析器 {config.parser}")
            continue

        version = parser.parse_version(response)
        print(f"  最新版本: {version}")

        # 获取当前版本
        pkgbuild_path = updater._get_pkgbuild_path(config.pkgbuild)
        from updater.pkgbuild_editor import PKGBUILDEditor
        editor = PKGBUILDEditor(pkgbuild_path)
        current_version = editor.get_pkgver()
        print(f"  当前版本: {current_version}")

        if version == current_version:
            print(f"  状态: 已是最新")
        else:
            print(f"  状态: 有更新可用")

if __name__ == "__main__":
    asyncio.run(check_versions())
```

运行:
```bash
uv run python check_version.py
```

### Q5: 如何更新单个包而不是全部？

**解决方案**:

```bash
# 方法 1: 使用 --package 参数
uv run main.py --package qq

# 方法 2: 修改 packages.yaml，临时注释掉其他包
```

### Q6: 如何查看详细的执行日志？

**解决方案**:

#### 方法 1: 修改代码添加日志

在 `scripts/main.py` 中添加:

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('update.log'),
        logging.StreamHandler()
    ]
)
```

#### 方法 2: 使用 debug 模式

```python
# 在代码中添加调试输出
async def update_package(self, package_name, package_config):
    print(f"[DEBUG] 开始更新包: {package_name}")
    print(f"[DEBUG] 配置: {package_config}")
    # ...
```

#### 方法 3: 使用 pdb 调试器

```python
import pdb

async def update_package(self, package_name, package_config):
    pdb.set_trace()  # 设置断点
    # ...
```

### Q7: 支持哪些架构？

**支持的架构**:
- `x86_64`: AMD64/Intel 64 位
- `aarch64`: ARM 64 位
- `loong64`: 龙芯 64 位
- `mips64el`: MIPS 64 位 Little Endian

**如何添加新架构**:

1. 在 `constants/constants.py` 添加:
```python
class ArchEnum(Enum):
    X86_64 = "x86_64"
    AARCH64 = "aarch64"
    RISCV64 = "riscv64"  # 新增
```

2. 在包配置中添加:
```yaml
arch:
  - x86_64
  - riscv64
```

3. 在 PKGBUILD 中添加对应的字段:
```bash
source_riscv64=('...')
sha512sums_riscv64=('...')
```

---

## 更新与维护

### Q8: 更新后 PKGBUILD 格式错误怎么办？

**问题描述**:
```
错误: PKGBUILD 语法错误
```

**原因**: 正则表达式替换可能破坏了格式

**解决方案**:

#### 方法 1: 手动修复
```bash
# 使用 git 恢复
cd packages/linuxqq-nt
git checkout PKGBUILD
```

#### 方法 2: 检查更新前备份
```bash
# 在更新前备份
cp PKGBUILD PKGBUILD.backup

# 更新后如果出错
cp PKGBUILD.backup PKGBUILD
```

#### 方法 3: 改进正则表达式
在 `updater/pkgbuild_editor.py` 中改进匹配模式:
```python
# 改进前
pattern = r"^pkgver=.*$"

# 改进后（更精确）
pattern = r"^pkgver=(?:[\"']?)([\d.]+)(?:[\"']?)$"
```

### Q9: 如何处理下载失败？

**问题描述**:
```
错误: 下载 x86_64 架构文件失败
```

**原因**:
- 网络问题
- URL 失效
- 服务器拒绝访问

**解决方案**:

#### 方法 1: 重试
```bash
# 再次运行
uv run main.py --package qq
```

#### 方法 2: 检查 URL
```python
# 手动测试 URL
curl -I https://example.com/file.deb
```

#### 方法 3: 使用代理
```bash
# 设置代理
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890

uv run main.py
```

#### 方法 4: 增加超时时间
在 `fetcher/fetcher.py` 中:
```python
def __init__(self, timeout: int = 30):  # 增加到 30 秒
    self.client = AsyncClient(timeout=timeout)
```

### Q10: 如何批量更新多个 AUR 包？

**解决方案**:

#### 方法 1: 使用工具更新所有包
```bash
uv run main.py
```

#### 方法 2: 脚本批量提交到 AUR
```bash
#!/bin/bash
# update_aur.sh

for pkg_dir in packages/*; do
    pkg_name=$(basename "$pkg_dir")
    echo "更新 $pkg_name"

    cd "$pkg_dir"

    # 检查是否有更新
    git diff PKGBUILD

    # 提交更新
    git add PKGBUILD
    git commit -m "upgpkg: update to $(grep pkgver PKGBUILD | cut -d= -f2)"
    git push

    cd ../..
done
```

#### 方法 3: 使用 aurutils
```bash
# 安装 aurutils
yay -S aurutils

# 批量更新
aur sync -u linuxqq-nt navicat17-premium-zh-cn
```

---

## 错误处理

### Q11: 解析器找不到怎么办？

**问题描述**:
```
错误: 找不到解析器 XXXParser
```

**原因**: 解析器未在 `PackageUpdater` 中注册

**解决方案**:

#### 步骤 1: 检查 ParserEnum
```python
# scripts/constants/constants.py
class ParserEnum(Enum):
    QQ = "QQParser"
    YOUR_PARSER = "YourParser"  # 确保存在
```

#### 步骤 2: 检查 PackageUpdater
```python
# scripts/core/package_updater.py
def __init__(self):
    self.parsers: dict[str, BaseParser] = {
        ParserEnum.QQ.value: QQParser(),
        ParserEnum.YOUR_PARSER.value: YourParser(),  # 确保注册
    }
```

#### 步骤 3: 导入解析器
```python
# scripts/core/package_updater.py
from parsers.your_parser import YourParser  # 确保导入
```

### Q12: 版本号解析失败怎么办？

**问题描述**:
```
错误: 无法解析版本号
```

**调试步骤**:

#### 1. 手动检查数据源
```bash
# 查看原始数据
curl -s https://example.com/api/version | head -100
```

#### 2. 测试解析器
```python
from parsers.qq import QQParser
import httpx

async def test_parser():
    parser = QQParser()
    async with httpx.AsyncClient() as client:
        response = await client.get("https://example.com/api/version")
        data = response.text
        print(f"数据: {data[:200]}")

        version = parser.parse_version(data)
        print(f"解析结果: {version}")

import asyncio
asyncio.run(test_parser())
```

#### 3. 修复解析器
根据实际数据格式调整 `parse_version()` 方法:
```python
def parse_version(self, response_data):
    # 添加调试输出
    print(f"响应数据长度: {len(response_data)}")
    print(f"前 200 字符: {response_data[:200]}")

    # 根据实际情况调整正则表达式
    match = re.search(r'你的正则表达式', response_data)
    return match.group(1) if match else None
```

### Q13: PKGBUILD 路径错误怎么办？

**问题描述**:
```
错误: PKGBUILD文件不存在: /path/to/PKGBUILD
```

**原因**: 路径配置错误或工作目录错误

**解决方案**:

#### 方法 1: 检查当前目录
```bash
# 确保在 scripts 目录
pwd  # 应该是 .../aur-packages/scripts

# 如果不在，切换到正确目录
cd scripts
```

#### 方法 2: 使用绝对路径
```yaml
# packages.yaml
pkgbuild: "/home/user/aur-packages/packages/linuxqq-nt/PKGBUILD"
```

#### 方法 3: 检查相对路径
```yaml
# 相对于项目根目录 (aur-packages/)
pkgbuild: "packages/linuxqq-nt/PKGBUILD"

# 而不是
pkgbuild: "../packages/linuxqq-nt/PKGBUILD"
```

### Q14: 校验和不匹配怎么办？

**问题描述**:
```
错误: SHA512 校验和不匹配
```

**原因**:
- 文件下载不完整
- 文件被篡改
- 校验和计算错误

**解决方案**:

#### 方法 1: 重新下载
```bash
# 删除旧文件
rm -f downloads/qq_*.deb

# 重新运行
uv run main.py --package qq
```

#### 方法 2: 手动验证
```python
from utils.hash import calculate_file_hash

# 计算实际校验和
hash = calculate_file_hash("downloads/qq_3.2.8_x86_64.deb", "sha512")
print(f"实际校验和: {hash}")
```

#### 方法 3: 从 PKGBUILD 读取校验和
```bash
# 查看当前校验和
grep sha512sums packages/linuxqq-nt/PKGBUILD
```

---

## 性能优化

### Q15: 如何加快更新速度？

**优化建议**:

#### 1. 并发处理包
修改 `core/package_updater.py`:
```python
async def update_all_packages(self):
    """并发更新所有包"""
    tasks = []
    for name, config in self.config.packages.items():
        task = self.update_package(name, config)
        tasks.append(task)

    # 并发执行
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # 统计结果
    success_count = sum(1 for r in results if r is True)
    print(f"更新完成: {success_count}/{len(results)} 个包更新成功")
```

#### 2. 使用缓存
```python
# 缓存版本号，避免重复请求
version_cache = {}

async def get_version_with_cache(fetcher, url):
    if url in version_cache:
        return version_cache[url]

    data = await fetcher.fetch_text(url)
    version = parse_version(data)
    version_cache[url] = version
    return version
```

#### 3. 限制并发数
```python
import asyncio

async def update_all_packages(self):
    semaphore = asyncio.Semaphore(3)  # 最多 3 个并发

    async def limited_update(name, config):
        async with semaphore:
            return await self.update_package(name, config)

    tasks = [limited_update(name, config)
             for name, config in self.config.packages.items()]
    await asyncio.gather(*tasks)
```

### Q16: 如何减少内存使用？

**优化建议**:

#### 1. 流式下载
```python
# 下载时直接计算校验和，不保存完整文件
async def download_and_hash(url):
    async with httpx.AsyncClient() as client:
        async with client.stream('GET', url) as response:
            hasher = hashlib.sha512()
            async for chunk in response.aiter_bytes():
                hasher.update(chunk)
            return hasher.hexdigest()
```

#### 2. 及时清理
```python
# 下载完成后立即删除
for arch, url in arch_urls.items():
    file_path = download_dir / filename

    # 下载
    await self._download_file(url, file_path)

    # 计算校验和
    checksum = await self._calculate_checksum(file_path)

    # 立即删除
    file_path.unlink()
```

#### 3. 使用生成器
```python
def iter_packages(self):
    """生成器遍历包，不一次性加载所有配置"""
    for name, config in self.config.packages.items():
        yield name, config
```

---

## 扩展开发

### Q17: 如何添加新软件包？

**详细步骤**:

请参考 [开发指南 - 添加新软件包](./04-development-guide.md#添加新软件包)

**快速步骤**:

1. 编辑 `packages.yaml`
2. 创建解析器
3. 注册解析器
4. 创建 PKGBUILD
5. 测试

### Q18: 如何创建自定义解析器？

**模板**:

```python
from parsers.base_parser import BaseParser
from constants.constants import ArchEnum
import re
import json

class CustomParser(BaseParser):
    """自定义解析器"""

    def parse_version(self, response_data):
        """解析版本号"""
        # 根据数据格式实现
        # JSON
        try:
            data = json.loads(response_data)
            return data.get("version")
        except:
            pass

        # HTML
        match = re.search(r'version["\s:]+([0-9.]+)', response_data)
        return match.group(1) if match else None

    def parse_url(self, arch, response_data):
        """解析下载 URL"""
        version = self.parse_version(response_data)
        if not version:
            return None

        # 根据版本号构造 URL
        return f"https://example.com/downloads/v{version}/app-{version}-{arch.value}.deb"
```

详细内容请参考 [开发指南 - 创建自定义解析器](./04-development-guide.md#创建自定义解析器)

### Q19: 如何贡献代码？

**贡献流程**:

1. **Fork 项目**
   ```bash
   # 在 GitHub 上 Fork 项目
   ```

2. **克隆 Fork**
   ```bash
   git clone https://github.com/yourusername/aur-packages.git
   cd aur-packages
   ```

3. **创建功能分支**
   ```bash
   git checkout -b feat/add-vscode-package
   ```

4. **编写代码**
   - 遵循代码规范
   - 添加测试
   - 更新文档

5. **提交代码**
   ```bash
   git add .
   git commit -m "feat(parser): 添加 VSCode 包解析器"
   ```

6. **推送到远程**
   ```bash
   git push origin feat/add-vscode-package
   ```

7. **创建 Pull Request**
   - 在 GitHub 上创建 PR
   - 填写 PR 模板
   - 等待审查

**代码审查清单**:
- [ ] 代码符合 PEP 8
- [ ] 所有测试通过
- [ ] 添加了文档
- [ ] 更新了配置
- [ ] 提交信息规范

---

## 其他问题

### Q20: 如何联系项目维护者？

**方式**:
- **GitHub Issues**: 报告 bug 或请求功能
- **GitHub Discussions**: 提问和讨论
- **Pull Request**: 贡献代码

### Q21: 项目是否支持 Windows？

**当前状态**: 仅支持 Linux

**原因**:
- PKGBUILD 是 Arch Linux 特有格式
- 工具设计用于维护 AUR 包

**未来计划**:
- 可能支持其他 Linux 发行版
- 不计划支持 Windows

### Q22: 如何获取项目最新版本？

```bash
# 拉取最新代码
git pull origin main

# 更新依赖
cd scripts
uv sync
```

---

**最后更新**: 2026-01-04

如有其他问题，欢迎在 GitHub Issues 中提出。

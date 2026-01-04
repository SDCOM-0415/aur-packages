"""URL 解析工具"""

from urllib.parse import urlparse
from pathlib import Path


def extract_filename_from_url(url: str) -> str:
    """
    从 URL 中提取文件名（包含扩展名）

    支持处理查询参数和片段标识符
    """
    parsed_url = urlparse(url)
    path = parsed_url.path

    # 从路径中提取文件名
    filename = Path(path).name

    # 如果无法提取文件名，使用 URL 的最后一部分
    if not filename:
        # 移除查询参数和片段
        filename = path.split("?")[0].split("#")[0]
        filename = filename.rstrip("/").split("/")[-1]

    return filename


def extract_extension_from_url(url: str) -> str:
    """
    从 URL 中提取文件扩展名（包含点号）

    支持复合扩展名（如 .tar.gz）和普通扩展名
    """
    filename = extract_filename_from_url(url)

    # 常见复合扩展名
    compound_extensions = {".tar.gz", ".tar.bz2", ".tar.xz", ".tar.zst"}
    for compound_ext in compound_extensions:
        if filename.endswith(compound_ext):
            return compound_ext

    # 返回单个扩展名或空字符串
    return Path(filename).suffix


def generate_download_filename(
    package_name: str,
    version: str,
    arch: str,
    url: str,
    default_extension: str = ".deb",
) -> str:
    """
    生成标准化的下载文件名

    格式: {package_name}_{version}_{arch}{extension}
    自动从 URL 提取扩展名，无扩展名时使用默认值
    """
    extension = extract_extension_from_url(url) or default_extension
    return f"{package_name}_{version}_{arch}{extension}"

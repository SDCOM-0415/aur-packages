"""
URL 工具函数
用于从 URL 中提取文件名、扩展名等信息
"""

from urllib.parse import urlparse
from pathlib import Path


def extract_filename_from_url(url: str) -> str:
    """
    从 URL 中提取文件名

    Args:
        url: 文件下载 URL

    Returns:
        文件名（包含扩展名）

    Examples:
        >>> extract_filename_from_url("https://example.com/file.tar.gz")
        "file.tar.gz"
        >>> extract_filename_from_url("https://example.com/path/to/app.AppImage")
        "app.AppImage"
    """
    # 解析 URL 获取路径部分
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
    从 URL 中提取文件扩展名

    Args:
        url: 文件下载 URL

    Returns:
        文件扩展名（包含点号，如 ".tar.gz", ".AppImage"）

    Examples:
        >>> extract_extension_from_url("https://example.com/file.tar.gz")
        ".tar.gz"
        >>> extract_extension_from_url("https://example.com/app.AppImage")
        ".AppImage"
        >>> extract_extension_from_url("https://example.com/file")
        ""
    """
    filename = extract_filename_from_url(url)

    # 使用 Path 提取扩展名
    # suffix 只获取最后一个扩展名，如 ".gz"
    # 对于复合扩展名（如 ".tar.gz"），需要特殊处理
    path_obj = Path(filename)

    # 常见的复合扩展名映射
    compound_extensions = {
        ".tar.gz": ".tar.gz",
        ".tar.bz2": ".tar.bz2",
        ".tar.xz": ".tar.xz",
        ".tar.zst": ".tar.zst",
    }

    # 检查是否是复合扩展名
    for compound_ext in compound_extensions:
        if filename.endswith(compound_ext):
            return compound_ext

    # 返回单个扩展名
    return path_obj.suffix


def generate_download_filename(
    package_name: str,
    version: str,
    arch: str,
    url: str,
    default_extension: str = "",
) -> str:
    """
    生成下载文件名（从 URL 提取扩展名）

    Args:
        package_name: 包名
        version: 版本号
        arch: 架构名称
        url: 下载 URL（用于提取扩展名）
        default_extension: 默认扩展名（如果 URL 没有扩展名时使用）
                         应包含点号（如 ".bin", ".download"），
                         默认为空字符串表示不添加扩展名

    Returns:
        生成的文件名

    Examples:
        >>> generate_download_filename("qq", "1.2.3", "x86_64", "https://example.com/qq.deb")
        "qq_1.2.3_x86_64.deb"
        >>> generate_download_filename("navicat", "17.0.0", "x86_64", "https://example.com/navicat.AppImage")
        "navicat_17.0.0_x86_64.AppImage"
        >>> generate_download_filename("pkg", "1.0.0", "x86_64", "https://example.com/download/file")
        "pkg_1.0.0_x86_64"
        >>> generate_download_filename("pkg", "1.0.0", "x86_64", "https://example.com/download", ".bin")
        "pkg_1.0.0_x86_64.bin"
    """
    # 从 URL 提取文件扩展名
    extension = extract_extension_from_url(url)

    # 如果没有扩展名且提供了默认扩展名，使用默认扩展名
    if not extension and default_extension:
        extension = default_extension

    # 生成文件名
    return f"{package_name}_{version}_{arch}{extension}"
